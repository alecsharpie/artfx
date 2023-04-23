import React, { useState, useEffect } from "react";
import "./Countdown.css";

const COUNTDOWN_TARGET_HOUR = 12; // 12:00pm
const COUNTDOWN_TARGET_TIMEZONE = "Australia/Melbourne";

function Countdown() {
  const [remainingTime, setRemainingTime] = useState(getRemainingTime());
  const [countdownEnded, setCountdownEnded] = useState(false);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setRemainingTime(getRemainingTime());
    }, 1000);
    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    if (
      remainingTime.hours === 0 &&
      remainingTime.minutes === 0 &&
      remainingTime.seconds === 0 &&
      !countdownEnded
    ) {
      setCountdownEnded(true);
      window.location.reload();
    }
  }, [remainingTime, countdownEnded]);

  function getRemainingTime() {
    const now = new Date();
    const target = new Date(
      now.getFullYear(),
      now.getMonth(),
      now.getDate(),
      COUNTDOWN_TARGET_HOUR,
      0,
      0,
      0
    );
    if (now.getTime() > target.getTime()) {
      target.setDate(target.getDate() + 1);
    }
    const targetUtc = target.toLocaleString("en-US", {
      timeZone: COUNTDOWN_TARGET_TIMEZONE,
    });
    const remainingMs = new Date(targetUtc) - now;
    const remainingSec = Math.floor(remainingMs / 1000);
    const remainingMin = Math.floor(remainingSec / 60);
    const remainingHrs = Math.floor(remainingMin / 60);
    return {
      hours: remainingHrs,
      minutes: remainingMin % 60,
      seconds: remainingSec % 60,
    };
  }

  const { hours, minutes, seconds } = remainingTime;
  return (
    <div className="countdown-container">
      <h2 className="countdown-title">New artwork in...</h2>
      <div className="countdown-timer">
        <div className="countdown-timer-item">
          {hours.toString().padStart(2, "0")}
        </div>
        <div className="countdown-timer-info">h</div>
        <div className="countdown-timer-separator">:</div>
        <div className="countdown-timer-item">
          {minutes.toString().padStart(2, "0")}
        </div>
        <div className="countdown-timer-info">m</div>
        <div className="countdown-timer-separator">:</div>
        <div className="countdown-timer-item">
          {seconds.toString().padStart(2, "0")}
        </div>
        <div className="countdown-timer-info">s</div>
      </div>
    </div>
  );;
}

export default Countdown;
