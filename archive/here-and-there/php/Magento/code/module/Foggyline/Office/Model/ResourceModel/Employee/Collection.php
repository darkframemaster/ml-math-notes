<?php
/* 
	$author = 'darkframexue';
	$description = "collection class for Employee entity.";
*/

namespace Foggyline\Office\Model\ResourceModel\Employee;

class Collection extends \Magento\Eav\Model\Entity\Collection\AbstractCollection{
	protected function _construct(){
		$this->_init(
			'Foggyline\Office\Model\Employee',
			'Foggyline\Office\Model\ResourceModel\Employee'	
		);
	}
}

?>
