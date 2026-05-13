# import time
# import threading
# from flask import Flask, render_template, redirect, url_for
# from gpiozero import LED, Buzzer, Button

# app = Flask(__name__)

# # Hardware config
# red_ns = LED(17); yellow_ns = LED(27); green_ns = LED(22)
# red_ew = LED(23); yellow_ew = LED(24); green_ew = LED(25)
# buzzer = Buzzer(5)
# ped_button = Button(6, bounce_time=0.1)
# ped_green = LED(13)
# ped_red = LED(19)

# def ped_button_pressed():
#     """Callback for pedestrian button press."""
#     global ped_request, ped_pending
#     with lock:
#         if not ped_request:  # Prevent multiple triggers
#             ped_request = True
#             ped_pending = True

# # Set up button event handler
# ped_button.when_pressed = ped_button_pressed

# # Global safe state
# rush_hour = False
# ped_request = False
# ped_active = False
# ped_red_flash = False
# ped_pending = False
# running = False
# lock = threading.Lock()

# NORMAL_TIMES = {"green": 10, "yellow": 3}
# RUSH_TIMES   = {"green": 20, "yellow": 3}

# def reset_lights():
#     """Sets a safe hardware baseline state."""
#     green_ns.off(); yellow_ns.off(); red_ns.on()
#     green_ew.off(); yellow_ew.off(); red_ew.on()
#     buzzer.off()
#     ped_green.off()
#     ped_red.off()

# def run_yellow_phase(yellow_led, times):
#     """Run a yellow phase."""
#     yellow_led.on()
#     time.sleep(times["yellow"])
#     yellow_led.off()

# def run_green_phase(green_led, red_to_off, red_leds, times):
#     """Run a green phase with pedestrian monitoring."""
#     red_to_off.off()
#     green_led.on()
#     for led in red_leds:
#         led.on()
    
#     total_green_time = times["green"]
#     time_elapsed = 0
#     ped_triggered = False
    
#     while time_elapsed < total_green_time and running:
#         time.sleep(0.1)
#         time_elapsed += 0.1
        
#         # Check for web request or button-triggered request
#         with lock:
#             if ped_request and not ped_triggered:
#                 ped_triggered = True
#                 if (total_green_time - time_elapsed) > 3:
#                     total_green_time = time_elapsed + 3
    
#     green_led.off()
#     return ped_triggered

# def traffic_cycle():
#     global rush_hour, ped_request, running, ped_active, ped_red_flash, ped_pending
    
#     reset_lights()
    
#     while True:
#         with lock:
#             if not running:
#                 reset_lights()
#                 break
#             current_rush = rush_hour
            
#         times = RUSH_TIMES if current_rush else NORMAL_TIMES

#         # --- Phase 1: North-South Green ---
#         if run_green_phase(green_ns, red_ns, [red_ew], times):
#             with lock:
#                 ped_request = True
#                 ped_pending = True
        
#         run_yellow_phase(yellow_ns, times)
#         if not running: continue
        
#         red_ns.on()

#         # --- Phase 2: Pedestrian Intermission ---
#         has_ped_req = False
#         with lock:
#             if ped_request:
#                 ped_request = False
#                 ped_pending = False  # Clear pending status
#                 has_ped_req = True
                
#         if has_ped_req and running:
#             with lock: ped_active = True
#             buzzer.on()
#             ped_green.on()
#             time.sleep(5)
#             buzzer.off()
#             ped_green.off()
            
#             with lock:
#                 ped_active = False
#                 ped_red_flash = True
                
#             for _ in range(5):
#                 if not running: break
#                 ped_red.toggle()
#                 time.sleep(0.5)
                
#             with lock: ped_red_flash = False
#             ped_red.off()
            
#         if not running: continue

#         # --- Phase 3: East-West Green ---
#         if run_green_phase(green_ew, red_ew, [red_ns], times):
#             with lock:
#                 ped_request = True
#                 ped_pending = True
        
#         run_yellow_phase(yellow_ew, times)
#         if not running: continue
        
#         red_ew.on()

# @app.route("/")
# def index():
#     return render_template("dashboard.html",
#                            rush=rush_hour,
#                            running=running,
#                            ns_red=red_ns.is_lit,
#                            ns_yellow=yellow_ns.is_lit,
#                            ns_green=green_ns.is_lit,
#                            ew_red=red_ew.is_lit,
#                            ew_yellow=yellow_ew.is_lit,
#                            ew_green=green_ew.is_lit,
#                            ped_green=ped_active,
#                            ped_led_green=ped_green.is_lit,
#                            ped_red_flash=ped_red_flash,
#                            ped_led_red=ped_red.is_lit,
#                            ped_pending=ped_pending)

# @app.route("/start")
# def start():
#     global running
#     with lock:
#         if not running:
#             running = True
#             threading.Thread(target=traffic_cycle, daemon=True).start()
#     return redirect(url_for("index"))

# @app.route("/stop")
# def stop():
#     global running
#     with lock:
#         running = False
#     reset_lights()
#     return redirect(url_for("index"))

# @app.route("/rush")
# def rush():
#     global rush_hour
#     with lock:
#         rush_hour = not rush_hour
#     return redirect(url_for("index"))

# @app.route("/ped")
# def ped():
#     global ped_request, ped_pending
#     with lock:
#         ped_request = True
#         ped_pending = True
#     return redirect(url_for("index"))

# if __name__ == "__main__":
#     reset_lights()
#     app.run(host="0.0.0.0", port=5000, debug=False)



# import threading
# import time
 
# from flask import Flask, redirect, render_template, url_for
# from gpiozero import Button, Buzzer, LED
 
# app = Flask(__name__)
 
# # Hardware config
# red_ns = LED(17)
# yellow_ns = LED(27)
# green_ns = LED(22)
# red_ew = LED(23)
# yellow_ew = LED(24)
# green_ew = LED(25)
# buzzer = Buzzer(5)
# ped_button = Button(6, bounce_time=0.1)
# ped_green = LED(13)
# ped_red = LED(19)
 
 
# def ped_button_pressed():
#     """Callback for pedestrian button press."""
#     global ped_request, ped_pending
#     with lock:
#         if not ped_request:  # Prevent multiple triggers
#             ped_request = True
#             ped_pending = True
 
 
# # Set up button event handler
# ped_button.when_pressed = ped_button_pressed
 
# # Global safe state
# rush_hour = False
# ped_request = False
# ped_active = False
# ped_red_flash = False
# ped_pending = False
# running = False
# lock = threading.Lock()
 
# NORMAL_TIMES = {"green": 10, "yellow": 3}
# RUSH_TIMES = {"green": 20, "yellow": 3}
 
 
# def reset_lights():
#     """Sets a safe hardware baseline state."""
#     green_ns.off()
#     yellow_ns.off()
#     red_ns.on()
#     green_ew.off()
#     yellow_ew.off()
#     red_ew.on()
#     buzzer.off()
#     ped_green.off()
#     ped_red.on()
 
 
# def run_yellow_phase(yellow_led, times):
#     """Run a yellow phase."""
#     yellow_led.on()
#     time.sleep(times["yellow"])
#     yellow_led.off()
 
 
# def run_green_phase(green_led, red_to_off, red_leds, times):
#     """Run a green phase with pedestrian monitoring."""
#     red_to_off.off()
#     green_led.on()
#     for led in red_leds:
#         led.on()
 
#     total_green_time = times["green"]
#     time_elapsed = 0
#     ped_triggered = False
 
#     while time_elapsed < total_green_time and running:
#         time.sleep(0.1)
#         time_elapsed += 0.1
 
#         # Check for web request or button-triggered request
#         with lock:
#             if ped_request and not ped_triggered:
#                 ped_triggered = True
#                 if (total_green_time - time_elapsed) > 3:
#                     total_green_time = time_elapsed + 3
 
#     green_led.off()
#     return ped_triggered
 
 
# def traffic_cycle():
#     global rush_hour, ped_request, running, ped_active, ped_red_flash, ped_pending
 
#     reset_lights()
 
#     while True:
#         with lock:
#             if not running:
#                 reset_lights()
#                 break
#             current_rush = rush_hour
 
#         times = RUSH_TIMES if current_rush else NORMAL_TIMES
 
#         # --- Phase 1: North-South Green ---
#         if run_green_phase(green_ns, red_ns, [red_ew], times):
#             with lock:
#                 ped_request = True
#                 ped_pending = True
 
#         run_yellow_phase(yellow_ns, times)
#         if not running:
#             continue
 
#         red_ns.on()
 
#         # --- Phase 2: Pedestrian Intermission ---
#         has_ped_req = False
#         with lock:
#             if ped_request:
#                 ped_request = False
#                 ped_pending = False  # Clear pending status
#                 has_ped_req = True
 
#         if has_ped_req and running:
#             with lock:
#                 ped_active = True
#             buzzer.on()
#             ped_green.on()
#             ped_red.off()
#             time.sleep(5)
#             buzzer.off()
#             ped_green.off()
 
#             with lock:
#                 ped_active = False
#                 ped_red_flash = True
 
#             for _ in range(5):
#                 if not running:
#                     break
#                 time.sleep(0.5)
 
#             with lock:
#                 ped_red_flash = False
#             ped_red.on()
 
#         if not running:
#             continue
 
#         # --- Phase 3: East-West Green ---
#         if run_green_phase(green_ew, red_ew, [red_ns], times):
#             with lock:
#                 ped_request = True
#                 ped_pending = True
 
#         run_yellow_phase(yellow_ew, times)
#         if not running:
#             continue
 
#         red_ew.on()
 
 
# @app.route("/")
# def index():
#     return render_template(
#         "dashboard.html",
#         rush=rush_hour,
#         running=running,
#         ns_red=red_ns.is_lit,
#         ns_yellow=yellow_ns.is_lit,
#         ns_green=green_ns.is_lit,
#         ew_red=red_ew.is_lit,
#         ew_yellow=yellow_ew.is_lit,
#         ew_green=green_ew.is_lit,
#         ped_green=ped_active,
#         ped_led_green=ped_green.is_lit,
#         ped_red_flash=ped_red_flash,
#         ped_led_red=ped_red.is_lit,
#         ped_pending=ped_pending,
#     )
 
 
# @app.route("/start")
# def start():
#     global running
#     with lock:
#         if not running:
#             running = True
#             threading.Thread(target=traffic_cycle, daemon=True).start()
#     return redirect(url_for("index"))
 
 
# @app.route("/stop")
# def stop():
#     global running
#     with lock:
#         running = False
#     reset_lights()
#     return redirect(url_for("index"))
 
 
# @app.route("/rush")
# def rush():
#     global rush_hour
#     with lock:
#         rush_hour = not rush_hour
#     return redirect(url_for("index"))
 
 
# @app.route("/ped")
# def ped():
#     global ped_request, ped_pending
#     with lock:
#         ped_request = True
#         ped_pending = True
#     return redirect(url_for("index"))
 
 
# if __name__ == "__main__":
#     reset_lights()
#     app.run(host="0.0.0.0", port=5000, debug=False)


import threading, time
from flask import Flask, redirect, render_template, url_for
from gpiozero import LED, Button, Buzzer

app = Flask(__name__)

# LEDs / hardware
red_ns, yellow_ns, green_ns = LED(17), LED(27), LED(22)
red_ew, yellow_ew, green_ew = LED(23), LED(24), LED(25)
ped_green, ped_red = LED(13), LED(19)
buzzer, ped_button = Buzzer(5), Button(6, bounce_time=0.1)

NORMAL = {"green": 10, "yellow": 3, "all_red": 2}
RUSH   = {"green": 20, "yellow": 3, "all_red": 2}

PED_WALK, PED_FLASHES, FLASH_INT = 5, 6, 0.5

rush_hour = ped_request = ped_active = ped_flash = ped_pending = running = False
phase = "stopped"
lock = threading.Lock()


def set_phase(p):
    global phase
    with lock: phase = p


def reset():
    for l in [green_ns, yellow_ns, green_ew, yellow_ew, ped_green]:
        l.off()
    for l in [red_ns, red_ew, ped_red]:
        l.on()
    buzzer.off()


def sleep_check(t, step=0.05):
    end = time.monotonic() + t
    while time.monotonic() < end:
        if not running: return False
        time.sleep(step)
    return True


def green_phase(green, red_off, red_on, times, name):
    global ped_request
    red_off.off()
    green.on()
    for r in red_on: r.on()

    set_phase(f"{name} green")
    total, elapsed, ped_seen = times["green"], 0, False

    while elapsed < total:
        if not running: break
        time.sleep(0.05)
        elapsed += 0.05

        with lock:
            if ped_request and not ped_seen:
                ped_seen = True
                total = min(total, elapsed + 3)

    green.off()
    return ped_seen


def yellow_phase(light, times, name):
    set_phase(f"{name} yellow")
    light.on()
    time.sleep(times["yellow"])
    light.off()


def all_red(times):
    set_phase("all red")
    red_ns.on(); red_ew.on()
    sleep_check(times["all_red"])


def pedestrian_phase():
    global ped_request, ped_pending, ped_active, ped_flash

    set_phase("pedestrian crossing")

    with lock:
        ped_request = ped_pending = False
        ped_active = True

    buzzer.on()
    ped_green.on()
    ped_red.off()
    sleep_check(PED_WALK)

    buzzer.off()
    ped_green.off()

    with lock:
        ped_active = False
        ped_flash = True

    for _ in range(PED_FLASHES):
        if not running: break
        ped_red.toggle()
        time.sleep(FLASH_INT)

    ped_flash = False
    ped_red.on()


def cycle():
    global running, ped_request, ped_pending

    reset()

    while running:
        times = RUSH if rush_hour else NORMAL

        for green, yellow, red, opp_red, name in [
            (green_ns, yellow_ns, red_ns, [red_ew], "N-S"),
            (green_ew, yellow_ew, red_ew, [red_ns], "E-W")
        ]:
            if green_phase(green, red, opp_red, times, name):
                ped_request = ped_pending = True

            if not running: break

            yellow_phase(yellow, times, name)
            red.on()
            all_red(times)

            if ped_request and running:
                pedestrian_phase()

    reset()
    set_phase("stopped")


def request_ped():
    global ped_request, ped_pending
    with lock:
        ped_request = ped_pending = True


ped_button.when_pressed = request_ped


@app.route("/")
def index():
    return render_template("dashboard.html",
        rush=rush_hour,
        running=running,
        phase=phase,
        ns_red=red_ns.is_lit,
        ns_yellow=yellow_ns.is_lit,
        ns_green=green_ns.is_lit,
        ew_red=red_ew.is_lit,
        ew_yellow=yellow_ew.is_lit,
        ew_green=green_ew.is_lit,
        ped_active=ped_active,
        ped_led_green=ped_green.is_lit,
        ped_red_flash=ped_flash,
        ped_led_red=ped_red.is_lit,
        ped_pending=ped_pending
    )


@app.route("/start")
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=cycle, daemon=True).start()
    return redirect(url_for("index"))


@app.route("/stop")
def stop():
    global running
    running = False
    return redirect(url_for("index"))


@app.route("/rush")
def rush():
    global rush_hour
    rush_hour = not rush_hour
    return redirect(url_for("index"))


@app.route("/ped")
def ped():
    request_ped()
    return redirect(url_for("index"))


if __name__ == "__main__":
    reset()
    app.run(host="0.0.0.0", port=5000)

    