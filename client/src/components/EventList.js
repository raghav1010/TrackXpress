import { useEffect, useState } from "react";
import JsonFormatter from 'react-json-formatter'

const EventList = () => {
    const jsonStyle = {
        propertyStyle: { color: 'red' },
        stringStyle: { color: 'green' },
        numberStyle: { color: 'darkorange' }
      }
  const [data, setData] = useState([]);
//  const sample = `{
//    string:"ABCDE",
//    "number":1,
//    "null":null,
//    "boolean":true,
//    "object":{
//       "string":"ABCDE",
//       "number":1,
//       "null":null,
//       "boolean":true
//    },
//    "array":[
//       1,
//       2,
//       3,
//       4,
//       {
//       "string":"ABCDE",
//       "number":1,
//       "null":null,
//       "boolean":true,
//          "array":[
//       1,
//       2,
//       3,
//       4,
//       {
//       "string":"ABCDE",
//       "number":1,
//       "null":null,
//       "boolean":true
//    }
//    ]
//    }
//    ]`

  useEffect(() => {
    (async function () {
       let response = fetch('http://0.0.0.0:5050/api/get/events', {
      method: 'GET',
      headers: {
        accept: 'application/json',
      },
    });
    console.log(response)
     let d = response.json();
//      let d = [
//        {
//            "description": "Whose order viewed",
//            "name": "Order Viewed 2",
//            "property_details": {
//                "currency": "INR",
//                "price": 100,
//                "product": "box"
//            }
//        },
//        {
//            "description": "Whose order viewed",
//            "name": "Order Viewed 3",
//            "property_details": {
//                "currency": "Dollar",
//                "price": 300,
//                "product": "fridge"
//            }
//        }
//    ]
      setData(d);
    })();
  }, []);

  return (
    <div className="event-list-wrapper">
      {data.length <= 0 && (
        <div className="form__wrapper--heading">No events found</div>
      )}
      {data.length > 0 && (
        <div>
          <div className="form__wrapper--heading">Events</div>
          <div className="event-list">
            {data.map((d,i) => {
              return (
                <div key={i} className="event-item"> {/* We should not use key prop but here we don't have any node changes */}
                  <div className="form-element">
                    <label>Name : </label>
                    <div>{d.name}</div>
                  </div>
                  <div className="form-element">
                    <label>Description : </label>
                    <div>{d.description}</div>
                  </div>
                  <div className="form-element">
                    <label>Rules : </label>
                    <div>
                      <JsonFormatter
                        json={d.property_details}
                        tabWith={3}
                        jsonStyle={jsonStyle}
                      />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default EventList;
