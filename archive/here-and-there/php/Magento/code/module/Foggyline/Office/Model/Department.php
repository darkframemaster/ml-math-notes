<?php

/*
	$author = 'darkframexue';
	$description = "Model class for Department entity";
*/

namespace Foggyline\Office\Model;

class Department extends \Magento\Framework\Model\AbstractModel{
	protected function _construct(){
		$this->_init('Foggyline\Office\Model\ResourceModel\Department');
	}
}

?>
