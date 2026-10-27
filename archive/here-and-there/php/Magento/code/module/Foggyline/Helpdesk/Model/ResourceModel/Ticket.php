<?php

namespace Foggyline\Helpdesk\Model\ResourceModel;

/*Resource class

	This class extends the
		\Magento\Framework\Model\ResourceModel\Db\AbstractDb class
	which further extends the
		\Magento\Framework\Model\ResourceModel\AbstractResource class
	This brings a lot of extra methods into our Ticket resource class:
		* load, delete, save, bommit, rollback ...

	The only actual requirement for us is to define the _construct
	method, through which we call the _init function that accepts two
	parameters.
		* The first parameter of the _init function specifies the
		table name foggyline_helpdesk_ticket.
		* The second parameter specifies identifying the ticket_id
		column within that table where we will be persisting data.	
*/
class Ticket extends \Magento\Framework\Model\ResourceModel\Db\AbstractDb
{
	/**
	 * Initialize resource model
	 * Get table name from config
	 * 
	 * @return void
	 */
	protected function _construct()
	{
		$this->_init('foggyline_helpdesk_ticket', 'ticket_id');
	}
}

?>
