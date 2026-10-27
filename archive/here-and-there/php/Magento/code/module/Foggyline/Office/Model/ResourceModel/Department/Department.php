<?php

/*
	$author = 'darkframexue';
	$description = 'collection class of Department entity';
*/

namespace Foggyline\Office\Model\ResourceModel\Department;

class Collection extends \Magento\Model\ResourceModel\Db\Collection\AbstractCollection{
	protected function _construct(){
		$this->_init(
			'Foggyline\Office\Model\Department',
			'Foggyline\Office\Model\ResourceModel\Department'
		);
	}
}

?>
