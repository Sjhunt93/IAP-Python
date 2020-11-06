from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_message_builder
from pythonosc import udp_client

import asyncio
import argparse
from time import sleep



class message:
    # root
    aserve = "/aserve/"

    # recive
    note = aserve + "note"
    control = aserve + "control"
    mod = aserve + "modwheel"
    pitchBend = aserve + "pitchbend"
    aftertouch = aserve + "aftertouch"
    pressure = aserve + "channelpressure"
    MIDI = aserve + "midi"

    #send
    oscilator = aserve + "osc"
    sample = aserve + "sample"
    pitchedSample = aserve + "samplepitch"
    setPixelGrid = aserve + "pixelgrid"
    pixelGridClicked = aserve + "clickedpixelgrid"
    loadsample = aserve + "loadsample"
    loadPitchedSample = aserve + "loadpitchedsample"
    lpf = aserve + "lpf"
    hpf = aserve + "hpf"
    bpf = aserve + "bpf"
    brf = aserve + "brf"
    loadDefaultSounds = aserve + "loaddefaults"
    reset = aserve + "reset"

    #special send (not avliable on some versions)
    mode = aserve + "mode"
    pan = aserve + "pan"

# we have to be careful here as Aserve wants explicit types so need to cast, otherwise 0 (for amp) becomes int when it needs to be float
class IAPComs:
    def __init__(self, oscclient):
        self.client = oscclient
    def aserveOscillator(self, chan, freq, amp, wave):
        self.client.send_message(message.oscilator, [int(chan), float(freq), float(amp), int(wave)])
    def aserveSleep(self, val):
        sleep(val/1000.0)
    def aserveLPF(self, cutoff):
        self.client.send_message(message.lpf, cutoff)

    # General startup info
    ip = "127.0.0.1"
    portIn = 9001

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=9002, help="The port the OSC server is listening on")
