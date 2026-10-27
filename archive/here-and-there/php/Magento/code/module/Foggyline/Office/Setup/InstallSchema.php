<?php

namespace Foggyline\Office\Setup;

use Magento\Framework\Setup\InstallSchemaInterface;
use Magento\Framework\Setup\ModuleContextInterface;
use Magento\Framework\Setup\SchemaSetupInterface;

class InstallSchema implements InstallSchemaInterface{
	public function install(SchemaSetupInterface $setup, 
	ModuleContextInterface $context)
	{
		$setup->startSetup();
		/* create our Department model entity table as follows:
			
			we are instructing Magento to create a table named 
			'foggyline_office_department',add entity and name cloumns to 
			it,and set the comment on the table.Assuming we are using the
			MySQL server, when code executes, the following SQL gets execu
			ted in the database:
			
			CREATE TABLE 'foggyline_office_department'(
				'entity_id' int(10) unsigned NOTNULL AUTO_INCREMENT 
				COMMENT 'Entity ID',
				'name' varchar(64) DEFAULT NULL COMMENT 'Name',
				PRIMARY KEY('entity_id')
			)ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf-8 COMMENT=
			'Foggyline Office Department Table'
		
			addColumn method takes five parameters,from column name,
			column data type,column length, array of additional options,
			and column description.However only column name and column
			data type are mandatory(强制的)

				you can find accepted column data types under 
			`/pathtoMagento/vendor/magento/framework/DB/Ddl/Table.php`,
			the `Magento\Framework\DB\Ddl\Table` class.List is as follow:

			boolean 	smallint 	integer 	bigint 		float 
			numeric 	decimal 	date		timestamp 	datatime 
			text 		blob 		varbinary
			
				An additional options array might contain some of the 
			following keys: 
		
			unsigned	precision	scale		unsigned	default
			nullable	primary		identity	auto_increment	
		
		
		*/
		$table = $setup->getConnection()
			->newTable($setup->getTable('foggyline_office_department'))
			->addColumn(
				'entity_id',
				\Magento\Framework\DB\Ddl\Table::TYPE_INTEGER,
				null,
				['identity'=>true, 'unsigned'=>true, 'nullable'=>false,
			'primary'=>true],
				'Entity ID'
			)
			->addColumn(
				'name',
				\Magento\Framework\DB\Ddl\Table::TYPE_TEXT,
				64,
				[],
				'Name'
			)
			->setComment('Foggyline Office Department Table');
		$setup->getConnection()->createTable($table);


		/*
			create 'foggyline_office_employee_entity' table for the 
			Employee entity.
		*/		
		$employeeEntity = \Foggyline\Office\Model\Employee::ENTITY;
		$table = $setup->getConnection()
			->newTable($setup->getTable($employeeEntity . '_entity'))
			->addColumn(
				'entity_id',
				\Magento\Framework\DB\Ddl\Table::TYPE_INTEGER,
				null,
				['identity'=>true, 'unsigned'=>true, 'nullable'=>false,
				'primary'=>true],
				'Entity ID'
			)
			->addColumn(
				'department_id',
				\Magento\Framework\DB\Ddl\Table::TYPE_INTEGER,
				null,
				['unsigned'=>true, 'nullable'=>false],
				'Department Id'
			)
			->addColumn(
				'email',
				\Magento\Framework\DB\Ddl\Table::TYPE_TEXT,
				64,
				[],
				'Email'
			)
			->addColumn(
				'first_name',
				\Magento\Framework\DB\Ddl\Table::TYPE_TEXT,
				64,
				[],
				'First Name'
			)
			->addColumn(
				'last_name',
				\Magento\Framework\DB\Ddl\Table::TYPE_TEXT,
				64,
				[],
				'Last Name'
			)
			->setComment('Foggyline Office Employee Table');
		$setup->getConnection()->createTable($table);
		
		/*
			EAV models scatter their data across several tables, three at
			a minimum.The table 'foggyline_office_employee_entity' that we
			just created is one of them.

			The other one is the core Magento 'eav_attribute' table.The 
			third table is not a single table,rather a list of multiple
			tables; one for each EAV type.These tables are the result of
			our install script.

			Information stored within the core Magento 'eav_attribute' 
			table is not the value of an attribute or anything like it;
			information stored there is an attribute's metadata.So how 
			does Magento know about our Employee attributes (dob, salary,
			service_years, vat_number, not)? It does not;not yet.We need
			to add the attributes into that table ourselves.

			Depending on the EAV attribute data tyepe,we need to create
			the following tabels:
				* foggyline_office_employee_entity_datetime
				* foggyline_office_employee_entity_decimal
				* foggyline_office_employee_entity_int
				* foggyline_office_employee_entity_text
				* foggyline_office_employee_entity_varchar
			
			The names of these attribute value tables come from a simple
			formula(公式),which says:
	
				{entity table name}+{_}+{eav_attribute.backend_type_value}
		
			if we look at the salary attribute,we need it to be a decimal
			value, thus it will get stored in 
				
				'foggyline_office_employee_entity_decimal'

			Now we will focus only on a single, decimal type table.
		*/

		$table = $setup->getConnection()
			->newTable(
				$setup->getTable($employeeEntity . '_entity_decimal')
			)
			->addColumn(
				'value_id',
				\Magento\Framework\DB\Ddl\Table::TYPE_INTEGER,
				null,
				['identity'=>true, 'nullable'=>false, 'primary'=>true],
				'Value ID'
			)
			->addColumn(
				'attribute_id',
				\Magento\Framework\DB\Ddl\Table::TYPY_SMALLINT,
				null,
				['unsigned'=>true, 'nullable'=>false, 'default'=>'0'],
				'Attribute ID'
			)
			->addColumn(
				'store_id',
				\Magento\Framework\DB\Ddl\Table::TYPE_SMALLINT,
				null,
				['unsigned'=>true, 'nullable'=>false, 'default'=>'0'],
				'Store ID'
			)
			->addColumn(
				'entity_id',
				\Magento\Framework\DB\Ddl\Table::TYPE_INTEGER,
				null,
				['unsigned'=>true, 'nullable'=>false, 'default'=>'0'],
				'Entity ID'
			)
			->addColumn(
				'value',
				\Magento\Framework\DB\Ddl\Table::TYPE_DECIMAL,
				'12,4',
				[],
				'Value'
			)
			->addIndex(
				$setup->getIdxName(
					$employeeEntity . '_entity_decimal',
					['entity_id', 'attribute_id', 'store_id'],
					\Magento\Framework\DB\Adapter\AdapterInterface::INDEX_TYPE_UNIQUE
				),
					['entity_id', 'attribute_id', 'store_id'],
					[type=>
					\Magento\Framework\DB\Adapter\AdapterInterface::INDEX_TYPE_UNIQUE]
			)
			->addIndex(
				$setup->getIdxName(
					$employeeEntity . '_entity_decimal',
					['store_id']
				),
				['store_id']
			)
			->addIndex(
				$setup->getIdxName(
					$employeeEntity . '_entity_decimal',
					['attribute_id']
				),
				['attribute_id']
			)
			->addForeignKey(
				$setup->getFkName(
					$employeeEntity . '_entity_decimal',
					'attribute_id',
					'eav_attribute',
					'attribute_id'
				),
				'attribute_id',
				$setup->getTable('eav_attribute'),
				'attribute_id',
				\Magento\Framework\DB\Ddl\Table::ACTION_CASCADE
			)
			->addForeignKey(
				$setup->getFkName(
					$employeeEntity . '_entity_decimal',
					'entity_id',
					$employeeEntity . '_entity',
					'entity_id'
				),
				'entity_id',
				$setup->getTable($employeeEntity . '_entity'),
				'entity_id',
				\Magento\Framework\DB\Ddl\Table::ACTION_CASCADE
			)
			->addForeignKey(
				$setup->getFkName(
					$employeeEntity . '_entity_decimal',
					'store_id',
					'store',
					'store_id'
				),
				'store_id',
				$setup->getTable('store'),
				'store_id',
				\Magento\Framework\DB\Ddl\Table::ACTION_CASCADE
			)
			->setComment('Employee Decimal Attribute Backend Table');
		$setup->getConnection()->createTable($table);
		/* The preceding code adds three indexes on the
			'foggyline_office_employee_entity_decimal' table,resulting in
			a SQL as follows:
			
			* UNIQUE KEY 
			'FOGGYLINE_OFFICE_EMPLOYEE_ENTT_DEC_ENTT_ID_ATTR_ID_STORE_ID' 
			('entity_id', 'attribute_id', 'store_id')
			* KEY 'FOGGYLINE_OFFICE_EMPLOYEE_ENTITY_DECIMAL_STORE_ID' 
			('store_id')
			* KEY 'FOGGYLINE_OFFICE_EMPLOYEE_ENTITY_DECIMAL_ATTRIBUTE_ID'
			('attribute_id')
		
			The preceding code also adds foreigh key relations into the
			'foggyline_office_employee_entity_decimal' table, resulting
			in a SQL as follows:
			
			* CONSTRAINT 'FK_D17982EDA1846BAA1F40E30694993801' FOREIGN KEY
			('entity_id') REFERENCES 'foggyline_office_employee_entity'
			('entity_id') ON DELETE CASCADE,
			* CONSTRAINT 'FOGGYLINE_OFFICE_EMPLOYEE_ENTITY_DECIMAL_STORE_
			ID_STORE_STORE_ID' FOREIGN KEY ('store_id') REFERENCES 'store'
			('store_id') ON DELETE CASCADE,
			* CONSTRAINT 'FOGGYLINE_OFFICE_EMPLOYEE_ENTT_DEC_ATTR_ID_EAV_
			ATTR_ATTR_ID' FOREIGN KEY ('attribute_id') REFERENCES 'eav_at
			tribute_id' ('attribute_id') ON DELETE CASCADE
		*/

		$setup->endSetup()
;
	}
}

?>
