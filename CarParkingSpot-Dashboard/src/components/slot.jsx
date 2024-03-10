import vehicleIcon from "../assets/images/vehicle.png";
import "../assets/styles/slot.css";

const Slot = ({ slotId, slotStatus }) => {
  return (
    <>
      <div className="col-12 col-sm-6 my-2 px-3">
        <div className="slot-container d-flex flex-wrap=">
          <div className="img-container col-3">
            <img src={vehicleIcon} width="80px" />
          </div>
          <div className="flex-fill">
            <div className="py-1 slot-id text-center">Slot ID: {slotId}</div>
            <div
              className={
                slotStatus
                  ? "py-1 text-center slot-status inactive"
                  : "py-1 text-center slot-status active"
              }
            >
              {slotStatus ? "Available" : "Unavailable"}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Slot;
