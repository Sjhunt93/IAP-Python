from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client

import asyncio
import aserve

# ------------------------------------------------------------------------------------------------------------------------------------
#           IAP
# ------------------------------------------------------------------------------------------------------------------------------------


class IAP:
    playBtn = False;
    def __init__(self, oscClient):
        self.client = oscClient
        self.aserve = aserve.IAPComs(oscClient)

        # ------------- Shared variables -----------------
        self.noteList = []
        self.lastNote = -1

        # ---

    # ------------- User defined functions -----------------
    # ------------- add more here
    #def myFunction():
    #    pass
    def mtof(note):
        return 440.0 * pow(2.0, (note-69.0)/12.0)

    # ------------- run function most of the code goes here -----------------
    async def run(self):
        self.aserve.aserveOscillator(0, 440.0, 0.3, 0)
        self.aserve.aserveSleep(1000)
        self.aserve.aserveOscillator(0, 0, 0, 0)

        while (1):
            if len(self.noteList) > 1:
                for n in self.noteList:
                    self.aserve.aserveOscillator(0, IAP.mtof(n), 0.3, 2)
                    self.aserve.aserveSleep(250)

            await asyncio.sleep(1) #wait and do nothing..

    # ------------- callbacks -----------------

    def callbackNote(self, note, velocity, channel):
        if velocity:
            self.aserve.aserveOscillator(0, IAP.mtof(note), 0.3, 2)
            self.lastNote = note
        #    self.noteList.append(note)
        elif self.lastNote == note:
            self.aserve.aserveOscillator(0, 0.0, 0.0, 2)

    def callbackMod(self, mod):
        # map to LPF filter 20-15,000
        self.aserve.aserveLPF((mod / 127.0) * 14800.0 + 20)


    def callbackCC(self, num, value):
        pass
    def callbackPitchBend(self, value):
        pass
    def callbackMIDI(self, status, d1, d2):
        pass
    def callbackPixelGrid(self, x, y):
        pass


# ------------------------------------------------------------------------------------------------------------------------------------
#           Setup
# ------------------------------------------------------------------------------------------------------------------------------------

#set up IAP class stuff
args = aserve.IAPComs.parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)
iap = IAP(client)

def note_handler(address, *args):
    iap.callbackNote(args[0], args[1], args[2])
def mod_handler(address, *args):
    iap.callbackMod(args[0])
def cc_handler(address, *args):
    iap.callbackCC(args[0], args[1])
def pb_handler(address, *args):
    iap.callbackPitchBend(args[0])

#finall set up the dispatchers
dispatcher = Dispatcher()

dispatcher.map(aserve.message.note, note_handler)
dispatcher.map(aserve.message.mod, mod_handler)
dispatcher.map(aserve.message.control, cc_handler)
dispatcher.map(aserve.message.pitchBend, pb_handler)
#dispatcher.map(aserve.message.MIDI, mod_handler)



async def init_main():
    server = AsyncIOOSCUDPServer((aserve.IAPComs.ip, aserve.IAPComs.portIn), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
    await iap.run()
    transport.close()  # Clean up serve endpoint

asyncio.run(init_main())
