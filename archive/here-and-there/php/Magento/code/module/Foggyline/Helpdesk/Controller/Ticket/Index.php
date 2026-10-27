<?php

namespace Foggyline\Helpdesk\Controller\Ticket;

class Index extends \Foggyline\Helpdesk\Controller\Ticket
{
	/*controller action
		
		Controller action code lives within the execute method of it's
		class.We simply extend from
			\Foggyline\Helpdesk\Controller\Ticket controller class 
		and define the necessary logic within the execute method.
		Simply calling loadlayout and renderLayour is enough to render
		the page on the frontend.
		
	*/
	public function execute()
	{
		$resultPage = $this->resultFactory->create(\Magento\Framework\Controller\ResultFactory::TYPE_PAGE);
		return $resultPage;
	}
}
?>
