<?php

namespace Foggyline\Helpdesk\Model\ResourceModel\Ticket;

/*Collection class

	This class extends the
		\Magento\Framework\Model\ResourceModel\Db\Collection\Abstraction class
	which further extends the
		\Magento\Framework\Data\Collection.
	The final parent collecion class the implements the following
	interface:
		\IteratorAggregate, \Countable, Magento\Framework\Option\ArrayInterface and Magento\Framework\Data\CollectionDataSourceInterface.
	
	Throught this deep inheritance, a large number of methods become
	available to our collection class, such as:
		* count, getAllIds, getColumnValues, getFirstItem ...

	The only actual requirement for us is to define the _construct
	method.Within the _construct method, we call the _init function
	to which we pass two parameters.
		* The first parameter specifies the Ticket medel class
		Foggyline\Helpdesk\Model\Ticket
		* The second parameter specifies the Ticket resource class
		Foggyline\Helpdesk\Model\ResourceModel\Ticket
*/
class Collection extends \Magento\Framework\Model\ResourceModel\Db\Collection\AbstractCollection
{
	/**
	 * Constructor
	 * Configures  collection
	 *
	 * @return void
	 */
	protected function _construct()
	{
		$this->_init('Foggyline\Helpdesk\Model\Ticket',
			'Foggyline\Helpdesk\Model\ResourceModel\Ticket');
	}
}
?>
