from src.event_apis.apis import EventTrackerAPI

Event_Tracker_API = EventTrackerAPI.as_view('kyc_doc_upload_api')

API_ROUTES = [
    ("/api/create/events", ["POST"], Event_Tracker_API),
    ("/api/get/events", ["GET"], Event_Tracker_API),
]