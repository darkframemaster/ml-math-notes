<?php

namespace Foggyline\Helpdesk\Setup;

use Magento\Framework\Setup\InstallSchemaInterface;
use Magento\Framework\Setup\ModuleContextInterface;
use Magento\Framework\Setup\SchemaSetupInterface;

/**
 * @codeCoverageIgnore
 */
class InstallSchema implements InstallSchemaInterface
{
	/*

	The InstallSchema class conforms to InstallSchemaInterface by impl
	ementing a single install method.Within this method, we start the 
	installer, create new tables, create new fields, add indexes and 
	foreign keys to the table, and finally ent the installer,as shown 
	in the following code:

	*/
	public function install(SchemaSetupInterface $setup, ModuleContextInterface $context)
	{
		$installer = $setup;

		$installer->startSetup();

		$table = $installer->getConnection()
			->newtable($installer->getTable('foggyline_helpdesk_ticket'))
			/*-------------- ->addColumn --------------*/
			->addColumn(
				'ticket_id',
				\Magento\Framework\DB\Ddl\Table::TYPE_INTEGER,
				null,
				['identity' => true, 'unsigned' => true, 'nullable' => false, 'primary' => true],
				'Ticket Id'
			)
			->addColumn(
				'customer_id',
				\Magento\Framework\DB\Ddl\Table::TYPE_INTEGER,
				null,
				['unsigned' => true],
				'Customer id'
			)
			->addColumn(
				'title',
				\Magenot\Framework\DB\Ddl\Table::TYPE_TEXT,
				null,
				['nullable' => true],
				'Title'
			)
			->addColumn(
				'severity',
				\Magento\Framework\DB\Ddl\Table::TYPE_SMALLINT,
				null,
				['nullable' => true],
				'Severity'
			)
			->addColumn(
				'create_at',
				\Magento\Framework\DB\Ddl\Table::TYPE_TIMESTAMP,
				null,
				['nullable' => true],
				'Created At'
			)
			->addColumn(
				'status'
				\Magento\Framework\DB\Ddl\Table::TYPE_SMALLINT,
				null,
				['nullable' => false],
				'Status'
			)
			/*-------------- ->addIndex ---------------*/
			->addIndex(
				$installer->getIdxName('foggyline_helpdesk_ticket', ['customer_id']),
				['customer_id']
			)
			/*-------------- ->addForeignKey ----------*/
			->addForeignKey(
				$installer->getFkName('foggyline_helpdesk_ticket', 'customer_id','customer_entity', 'entity_id'),
				'customer_id',
				$installer->getTable('customer_entity'),
				'entity_id',
				\Magento\Framework\DB\Ddl\Table::ACTION_SET_NULL
			)
			->setComment('Foggyline Helpdesk Ticket');

		$installer->getConnection()->createTable('$table');

		$installer->endSetup();
	}
}
