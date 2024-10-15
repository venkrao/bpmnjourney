import asyncio
from pyzeebe import ZeebeWorker, create_insecure_channel, ZeebeTaskRouter

import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

# Zeebe client configuration
ZEEBE_ADDRESS = "localhost"
ZEEBE_PORT = "26500"

# Create a TaskRouter to register tasks
task_router = ZeebeTaskRouter()

# Simulated databases
warranty_database = {
    "WARR-111": {"valid": True},
    "WARR-000": {"valid": False},
}

repairs_database = dict()
repair_notifications_database = dict()
paid_service_database = dict()
service_quality_survey_notifications_database = dict()


def is_warranty_active(warranty_number: str):
    warranty_info = warranty_database.get(warranty_number)
    
    if warranty_info and warranty_info.get("valid"):
        return True
    return False


@task_router.task(task_type="record_repair_completion")
async def task_record_repair_completion(warranty_number: str):
    logger.debug(f"Recording repair completion in database: {warranty_number}")
    if not warranty_number:
        raise ValueError("Warranty number is missing")

    repairs_database[warranty_number] = {"repair_completed": True}
    return {warranty_number: repairs_database[warranty_number]}


@task_router.task(task_type="repair_feedback_survey_notification")
async def task_repair_feedback_survey_notification(warranty_number: str):
    logger.debug(f"Sending repair quality feedback survey to customer: {warranty_number}")
    if not warranty_number:
        raise ValueError("Warranty number is missing")

    service_quality_survey_notifications_database[warranty_number] = {"repair_completed": True}
    return {warranty_number: service_quality_survey_notifications_database[warranty_number]}


@task_router.task(task_type="repair_complete_notification")
async def task_repair_complete_notification(warranty_number: str):
    logger.debug(f"Sending repair completion notification to customer: {warranty_number}")
    if not warranty_number:
        raise ValueError("Warranty number is missing")

    repair_notifications_database[warranty_number] = {"repair_completed": True}
    return {warranty_number: repair_notifications_database[warranty_number]}


@task_router.task(task_type="solicit_paid_service")
async def task_solicit_paid_service(warranty_number: str):
    logger.debug(f"Soliciting paid service: {warranty_number}")
    if not warranty_number:
        raise ValueError("Warranty number is missing")

    paid_service_database[warranty_number] = {"paid_service_offered": True}
    return paid_service_database[warranty_number]


@task_router.task(task_type="check_warranty_validity")
async def check_warranty(warranty_number: str):
    logger.debug(f"Checking warranty for order: {warranty_number}")
    
    if not warranty_number:
        raise ValueError("Warranty number is missing")

    warranty_active = is_warranty_active(warranty_number)

    return {
        "warranty_active": warranty_active,
    }


async def main():
    print("Washsuperwell Limited.")
    channel = create_insecure_channel(hostname=ZEEBE_ADDRESS, port=ZEEBE_PORT)
    worker = ZeebeWorker(channel)
    worker.include_router(task_router)

    print("Repair Washing Machine. Waiting for tasks...")
    await worker.work()


if __name__ == "__main__":
    asyncio.run(main())
