import asyncio
from pyzeebe import ZeebeClient, create_insecure_channel
import sys

async def main():
    # Set up Zeebe client
    channel = create_insecure_channel("localhost", 26500)
    client = ZeebeClient(channel)

    # Mock function to simulate customer reply
    async def mock_customer_reply(warranty_number: str, customer_response: bool):
        print(f"Mocking customer reply for email_id: {warranty_number}")
        
        customer_response = True if customer_response == "True" else False
        # This sends a message to Zeebe that will correlate with the Message Intermediate Catch Event
        await client.publish_message(
            name="response_paid_service",
            correlation_key=warranty_number,
            variables={"paid_service_ok": bool(customer_response)}
        )

    # Simulate the customer reply (use the email_id from your process)
    warranty_number = sys.argv[1]
    customer_response = sys.argv[2]

    await mock_customer_reply(warranty_number, customer_response)

if __name__ == "__main__":
    asyncio.run(main())
