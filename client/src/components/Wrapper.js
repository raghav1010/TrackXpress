import { useState } from "react";
import Events from "./Events";
import Tracking from "./Tracking";
import { DEFAULT_EVENTS } from "./utils/presets";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import EventList from "./EventList";

const Wrapper = () => {
  const [trackingName, setTrackingName] = useState("");
  const [trackingDecription, setTrackingDecription] = useState("");
  const [trackingErrors, setTrackingErrors] = useState({});
  const [events, setEvents] = useState(DEFAULT_EVENTS);
  const [eventErrors, setEventErrors] = useState([{}]);
  const [showAll, setShowAll] = useState(false);

  async function onSave() {
    // Manipulate Data here
    console.log(
      "Saving",
      trackingName,
      trackingDecription,
      events,
      trackingErrors,
      eventErrors
    );
    if (Object.keys(trackingErrors).length > 0) return;
    let valid = true;
    for (let j = 0; j < eventErrors.length; j++) {
      if (Object.keys(eventErrors[j]).length > 0) {
        valid = false;
        break;
      }
    }
    if (!valid) return;

    const payload = getPayload();

    const response = await fetch("http://localhost:5050/api/create/events",
    {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: {
        accept: 'application/json'
      }
    })
    const data = await response.json();
    console.log("DATA", data)
    if (data.error) {
      toast(data.error.message);
    } else {
      toast(data.result.message);
    }
  }

  function getPayload() {
    return {
        tracking_plan: {
            display_name: trackingName,
            description: trackingDecription,
            source: 'mixpanel3',
            rules: {
                events
            }
        }
    }
  }

  function onShow() {
    const s = !showAll;
    setShowAll(s);
  }

  return (
    <>
      <div className="wrapper">
        <form>
          {!showAll && <><Tracking
            trackingName={trackingName}
            setTrackingName={setTrackingName}
            trackingDecription={trackingDecription}
            setTrackingDecription={setTrackingDecription}
            trackingErrors={trackingErrors}
            setTrackingErrors={setTrackingErrors}
          />
          <hr></hr>
          <Events
            events={events}
            setEvents={setEvents}
            eventErrors={eventErrors}
            setEventErrors={setEventErrors}
          /></>}
          {showAll && <EventList />}
          <div className="btn-container">
            {!showAll && (
              <button
                style={{ marginRight: "5px" }}
                type="button"
                className="add-btn"
                onClick={onSave}
              >
                Save
              </button>
            )}

            <button type="button" className="add-btn" onClick={onShow}>
              {showAll ? "Add Entity" : "Show All"}
            </button>
          </div>
        </form>
      </div>
      <ToastContainer />
    </>
  );
};

export default Wrapper;
