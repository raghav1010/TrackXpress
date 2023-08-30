import { useEffect } from "react";
import { alphanumericRegex, uuidv4 } from "./utils/presets";

const Events = ({ events, setEvents, eventErrors, setEventErrors }) => {
  function setFormValue($event, key, index) {
    const eventsCopy = [...events];
    eventsCopy[index][key] = $event.target.value;
    setEvents(eventsCopy);
  }

  function addEvents() {
    const newEvents = [...events];
    newEvents.push({
      id: uuidv4(),
      name: "",
      description: "",
      rules: "",
    });
    const eventErrorsCopy = eventErrors.map((e) => {
      return { ...e };
    });
    eventErrorsCopy.push({
      required: true,
      namePatternMismatch: true,
      JSONpatternMismatch: true,
    });
    setEventErrors(eventErrorsCopy);
    setEvents(newEvents);
  }

  useEffect(() => {
    const eventErrorsCopy = eventErrors.map((e) => {
      return { ...e };
    });
    events.forEach((event, i) => {
      if (!event.name?.trim() || !event.rules?.trim()) {
        eventErrorsCopy[i].required = true;
      } else {
        delete eventErrorsCopy[i].required;
      }
      setEventErrors(eventErrorsCopy);

      if (event.name?.trim()) {
        if (!alphanumericRegex.test(event.name)) {
          eventErrorsCopy[i].namePatternMismatch = true;
        } else {
          delete eventErrorsCopy[i].namePatternMismatch;
        }
      }

      try {
        JSON.parse(event.rules);
        delete eventErrorsCopy[i].JSONpatternMismatch;
      } catch (error) {
        eventErrorsCopy[i].JSONpatternMismatch = true;
      }
    });

    console.log(eventErrorsCopy);
  }, [events]);

  return (
    <div className="form__wrapper">
      <div
        className="form__wrapper--heading"
        style={{
          marginTop: "2rem",
        }}
      >
        Events
      </div>
      <div className="form__wrapper--form">
        <div className="form-events">
          {events.map((event, i) => (
            <>
              <div className="form-event" key={event.id}>
                <div className="form-element">
                  <label>Name : </label>
                  <div className="input-container">
                    <input
                      type="text"
                      onChange={($ev) => setFormValue($ev, "name", i)}
                      value={event.name}
                      placeholder="Order Placed"
                    />
                  </div>
                </div>
                <div className="form-element">
                  <label>Description : </label>
                  <div className="input-container">
                    <input
                      type="text"
                      onChange={($ev) => setFormValue($ev, "description", i)}
                      value={event.description}
                      placeholder="An order is placed"
                    />
                  </div>
                </div>
                <div className="form-element">
                  <label>Rules : </label>
                  <div className="input-container">
                    <textarea
                      rows={7}
                      onChange={($ev) => setFormValue($ev, "rules", i)}
                      value={event.rules}
                      placeholder="{ JSON SCHEMA }"
                    />
                  </div>
                </div>
              </div>
              <div className="error-message">
                {eventErrors[i].required ? (
                  <>Name and Rules must not be empty</>
                ) : eventErrors[i].namePatternMismatch ? (
                  <>Name must be alphanumeric</>
                ) : eventErrors[i].JSONpatternMismatch ? (
                  <>JSON must be a valid schema</>
                ) : (
                  <></>
                )}
              </div>
            </>
          ))}
        </div>
        <button type="button" onClick={() => addEvents()} className="add-btn">
          <span>&#43;</span>
        </button>
      </div>
    </div>
  );
};

export default Events;
