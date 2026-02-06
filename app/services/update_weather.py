from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger



scheduler = AsyncIOScheduler()



def start_updater_weather(interval_min = 15) -> bool:
    from ..crud import update_all_weather
    if not scheduler.running:
        scheduler.add_job(
            update_all_weather,
            trigger=IntervalTrigger(minutes=interval_min),
            id="update_weather",
            name="Обновление погоды всех городов",
            replace_existing=True,
        )
        scheduler.start()
    
    if scheduler.running:
        return True
    return False

def shutdown_updater_weather() -> bool:
    if scheduler.running:
        scheduler.shutdown()
    if scheduler.running:
        return False
    return True
