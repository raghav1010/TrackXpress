import { useEffect } from "react";
import { alphanumericRegex } from "./utils/presets";

const Tracking = ({
  trackingName,
  setTrackingName,
  trackingDecription,
  setTrackingDecription,
  trackingErrors,
  setTrackingErrors,
}) => {
  function setFormValue($event, key) {
    const value = $event.target.value;
    if (key === "trackingName") {
      setTrackingName(value);
    }
    if (key === "trackingDecription") {
      setTrackingDecription(value);
    }
  }

  useEffect(() => {
    let existing = { ...trackingErrors };
    delete existing.nameRequired;
    if (trackingName.trim()) {
      if (!alphanumericRegex.test(trackingName)) {
        existing.patternMismatch = true;
      } else {
        delete existing.patternMismatch;
      }
    } else {
      delete existing.patternMismatch;
      if (trackingDecription.trim()) {
        existing.nameRequired = true;
      } else {
        delete existing.nameRequired;
      }
    }
    setTrackingErrors(existing);
    console.log(existing);
  }, [trackingName, trackingDecription]);

  return (
    <div className="form__wrapper" style={{ marginBottom: '1.5rem' }}>
      <div className="form__wrapper--heading">Add Tracking Plan</div>
      <div className="form__wrapper--form">
        <div className="form-element">
          <label>Name : </label>
          <div className="input-container">
            <input
             
              type="text"
              onChange={($event) => setFormValue($event, "trackingName")}
              value={trackingName}
              placeholder="Tracking Plan 1"
            />
            <div className="error-message">
              {trackingErrors.nameRequired ? (
                <>Name must not be empty</>
              ) : trackingErrors.patternMismatch ? (
                <>Name must be alphanumeric</>
              ) : (
                <></>
              )}
            </div>
          </div>
        </div>
        <div className="form-element">
          <label>Description : </label>
          <div className="input-container">
          <input
            type="text"
            onChange={($event) => setFormValue($event, "trackingDecription")}
            value={trackingDecription}
            placeholder="First Tracking Plan"
          />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tracking;
