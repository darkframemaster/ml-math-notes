<?php

namespace Foggyline\Helpdesk\Model;

/*MODEL class

	This script defined the Ticket entity model class

	This class extends the
		\Magento\Framework\Model\AbstractModel class
	which further extends the 
		\Magento\Framework\Model\Object class
	This brings a lot of extra methods into our Ticket model class,
	such as
		* load, delete, save, toArray, toJson, toString, toXml ...
	
	The only actual requirement for us is to define the _construct 
	method that, through the _init function call, specifies the
	resource class the model will be using when persisting data.

	Param of the _init function:
		* string: namespace of the resource class
*/
class Ticket extends \Magento\Framework\Model\AbstractModel
{
	const STATUS_OPENED = 1;
	const STATUS_CLOSED = 2;

	const SEVERITY_LOW = 1;
	const SEVERITY_MEDIUM = 2;
	const SEVERITY_HIGH = 3;

	protected static $statusesOptions = [
		self::STATUS_OPENED => 'Opened',
		self::STATUS_CLOSED => 'Closed',
	];

	protected static $severitiesOptions = [
		self::SEVERITY_LOW => 'Low',
		self::SEVERITY_MEDIUM => 'medium',
		self::SEVERITY_HIGH => 'high',
	];

	/**
	 * Initialize resource model
	 * @return void
	 */
	protected function _construct()
	{
		$this->_init('Foggyline\Helpdesk\Model\ResourceModel\Ticket');
	}

	public static function getSeveritiesOptionArray()
	{
		return self::$severitiesOptions;
	}

	public function getStatusAsLabel()
	{
		return self::$statusesOptions[$this->getStatus()];
	}

	public function getSeverityAsLabel()
	{
		return self::$severitiesOptions[$this->getSeverity()];
	}
	
}
