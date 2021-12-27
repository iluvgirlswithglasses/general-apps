from datetime import datetime, timedelta
import time
import os

# utils
def calc_time(at: str):
    alarm_time = timedelta(days=0, hours=int(at[0:2]), minutes=int(at[2:4]), seconds=0)
    now = datetime.now()
    cr_time = timedelta(days=0, hours=now.hour, minutes=now.minute, seconds=now.second)
    #
    d = int((alarm_time - cr_time).total_seconds())
    if d > 0: return d
    return d + 86400

# drivers
def run(secs: int, track_path: str):
    time.sleep(secs)
    os.system('mpv "{}" --no-audio-display'.format(
        track_path
    ))


if __name__ == '__main__':
    alarm_cd = calc_time(input("Alarm at (HHMM)(24h format): "))
    track_path = input("Alarm sound: ")
    print(f"alarm is set for {alarm_cd} secs !")
    run(alarm_cd, track_path)
