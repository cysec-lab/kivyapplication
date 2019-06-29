


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition

import os
from collections import namedtuple

import PIL
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from PIL import ImageOps
from pyzbar import pyzbar

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

from kivy.properties import StringProperty
from kivy.lang import Builder
#import json
import web3

from web3 import Web3,HTTPProvider
#from solc import compile_source
from web3.contract import ConciseContract
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import StringProperty,ListProperty,BooleanProperty
from kivy.utils import get_color_from_hex

# Solidity source code
# contract_source_code = '''
# pragma solidity ^0.4.23;
#  contract multisign{
#      mapping(uint256=>bool)private comfirmed ;
#      mapping(uint256=>bool)private register ;
#      mapping(uint256=>address)private uploadadd;
#      function receiveHash(address _from,uint256 _hash ,uint i)returns(bool){ //i=0,want to be checked.    i = 1,want to be comfirmed
#          if(i==0)
#          {
#              register[_hash] = true;
#              uploadadd[_hash] = _from;
#              return true;
#          }
#          else if(i==1&&(_from != uploadadd[_hash]))
#          {
#              if( register[_hash] == true)
#              {
#                  comfirmed[_hash] = true;
#                  return true;
#              }
#              else
#                  revert();
#          }
#          else
#              revert();
#      }
#     function checkhash(uint256 _hash)returns(bool)
#     {
#         return comfirmed[_hash];
#     }
#  }
# '''
#
# compiled_sol = compile_source(contract_source_code)  # Compiled source code
# contract_interface = compiled_sol['<stdin>:multisign']
# print(contract_interface['abi'])
# print(contract_interface['bin'])


# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://74bf98d6.ngrok.io"))

# set pre-funded account as sender
#w3.eth.defaultAccount = w3.eth.accounts[0]

# Instantiate and deploy contract
mutisign = w3.eth.contract(abi=[{'constant': False, 'inputs': [{'name': '_hash', 'type': 'uint256'}], 'name': 'checkhash', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': '_from', 'type': 'address'}, {'name': '_hash', 'type': 'uint256'}, {'name': 'i', 'type': 'uint256'}], 'name': 'receiveHash', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}],
                           bytecode='608060405234801561001057600080fd5b506102d0806100206000396000f30060806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063167747b814610051578063c7f47bae14610096575b600080fd5b34801561005d57600080fd5b5061007c60048036038101908080359060200190929190505050610105565b604051808215151515815260200191505060405180910390f35b3480156100a257600080fd5b506100eb600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001909291908035906020019092919050505061012e565b604051808215151515815260200191505060405180910390f35b600080600083815260200190815260200160002060009054906101000a900460ff169050919050565b6000808214156101be57600180600085815260200190815260200160002060006101000a81548160ff021916908315150217905550836002600085815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506001905061029d565b60018214801561022d57506002600084815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff1614155b1561029857600115156001600085815260200190815260200160002060009054906101000a900460ff161515141561029357600160008085815260200190815260200160002060006101000a81548160ff0219169083151502179055506001905061029d565b600080fd5b600080fd5b93925050505600a165627a7a72305820bd093e2688661cb415a3375458242c1a12b39784d8db5b89802997c4111b80d90029')

# Submit the transaction that deploys the contract
#tx_hash = mutisign.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
#tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#print(tx_receipt.contractAddress)


Mutisign = w3.eth.contract(
    address='0x9cf4DED3BfeE72c2Ca6FA5C5e6de7c22aAb25535',
    abi=[{'constant': False, 'inputs': [{'name': '_hash', 'type': 'uint256'}], 'name': 'checkhash', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': '_from', 'type': 'address'}, {'name': '_hash', 'type': 'uint256'}, {'name': 'i', 'type': 'uint256'}], 'name': 'receiveHash', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}],
)



Builder.load_file('app.kv')


class TextWidget(Widget):
    text = StringProperty()
    text2 = StringProperty()

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
    def buttonClicked0(self):
        #self.text =  self.ids["address_box"].text

        self.ids.address_box.text = self.text2
        self.ids.hash_box.text = self.text
        #self.text2 = self.ids["address_box"].text
        #self.text = self.ids["hash_box"].text
        self.ids.label1.text = "upload is done!"
        self.ids.label2.text = ""
        #self.ids.label2.text = self.text2
        try:
            w3.eth.defaultAccount = Web3.toChecksumAddress(self.text2)
            tx_hash = Mutisign.functions.receiveHash(Web3.toChecksumAddress(self.text2),
                                                 int((self.text), 16),
                                                 0).transact()
            w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_hash)
        except:
            self.ids.label1.text = "upload error"
            self.ids.label2.text = "please check the address or hash is valid"
        finally:
            pass
    def buttonClicked1(self):

        self.ids.address_box.text = self.text2
        self.ids.hash_box.text = self.text
        #self.text2 = self.ids["address_box"].text
        #self.text = self.ids["hash_box"].text
        self.ids.label1.text = "sign is done!"
        self.ids.label2.text = ""
        #self.ids.label2.text = self.text2
        try:
            w3.eth.defaultAccount = Web3.toChecksumAddress(self.text2)
            tx_hash = Mutisign.functions.receiveHash(Web3.toChecksumAddress(self.text2),
                                                 int((self.text), 16),
                                                 1).transact()
            w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_hash)
        except:
            self.ids.label1.text = "sign error"
            self.ids.label2.text = "please check the address or hash is valid"
        finally:
            pass
    def buttonClickedch(self):
        self.ids.hash_box.text = self.text
        #self.text = self.ids["hash_box"].text
        self.ids.label1.text = ''
        try:
            temp = Mutisign.functions.checkhash(int((self.text), 16)).call()
            if(temp):
                self.ids.label2.text = 'this file is true'
            else:
                self.ids.label2.text = 'this file is false'
        except:
            self.ids.label1.text = "hash error"
            self.ids.label2.text = "please check the hash is valid"
        finally:
            pass


class ZBarCam(AnchorLayout):
    """
    Widget that use the Camera and zbar to detect qrcode.
    When found, the `codes` will be updated.
    """
    resolution = ListProperty([640, 480])

    symbols = ListProperty([])
    Symbol = namedtuple('Symbol', ['type', 'data'])
    # checking all possible types by default
    code_types = ListProperty(set(pyzbar.ZBarSymbol))
    codedata = StringProperty()

    def __init__(self, **kwargs):
        self._request_android_permissions()
        # lazy loading the kv file rather than loading at module level,
        # that way the `XCamera` import doesn't happen too early
        Builder.load_file(os.path.join(MODULE_DIRECTORY, "zbarcam.kv"))
        super(ZBarCam, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self._setup())

    def _setup(self):
        """
        Postpones some setup tasks that require self.ids dictionary.
        """
        self._remove_shoot_button()
        self._enable_android_autofocus()
        self.xcamera._camera.bind(on_texture=self._on_texture)
        # self.add_widget(self.xcamera)

    def _remove_shoot_button(self):
        """
        Removes the "shoot button", see:
        https://github.com/kivy-garden/garden.xcamera/pull/3
        """
        xcamera = self.xcamera
        shoot_button = xcamera.children[0]
        xcamera.remove_widget(shoot_button)

    def _enable_android_autofocus(self):
        """
        Enables autofocus on Android.
        """
        if not self.is_android():
            return
        camera = self.xcamera._camera._android_camera
        params = camera.getParameters()
        params.setFocusMode('continuous-video')
        camera.setParameters(params)

    def _request_android_permissions(self):
        """
        Requests CAMERA permission on Android.
        """
        if not self.is_android():
            return
        from android.permissions import request_permission, Permission
        request_permission(Permission.CAMERA)

    @classmethod
    def _fix_android_image(cls, pil_image):
        """
        On Android, the image seems mirrored and rotated somehow, refs #32.
        """
        if not cls.is_android():
            return pil_image
        pil_image = pil_image.rotate(90)
        pil_image = ImageOps.mirror(pil_image)
        return pil_image

    def _on_texture(self, instance):
        self.symbols = self._detect_qrcode_frame(
            texture=instance.texture, code_types=self.code_types)

    @classmethod
    def _detect_qrcode_frame(cls, texture, code_types):
        image_data = texture.pixels
        size = texture.size
        # Fix for mode mismatch between texture.colorfmt and data returned by
        # texture.pixels. texture.pixels always returns RGBA, so that should
        # be passed to PIL no matter what texture.colorfmt returns. refs:
        # https://github.com/AndreMiras/garden.zbarcam/issues/41
        pil_image = PIL.Image.frombytes(mode='RGBA', size=size,
                                        data=image_data)
        pil_image = cls._fix_android_image(pil_image)
        symbols = []
        codes = pyzbar.decode(pil_image, symbols=code_types)
        for code in codes:
            symbol = ZBarCam.Symbol(type=code.type, data=code.data)
            symbols.append(symbol)
            ZBarCam.codedata = code.data.decode("utf-8")
        return symbols

    @property
    def xcamera(self):
        return self.ids['xcamera']

    def start(self):
        self.xcamera.play = True

    def stop(self):
        self.xcamera.play = False

    @staticmethod
    def is_android():
        return platform == 'android'

    @staticmethod
    def is_ios():
        return platform == 'ios'

class qrcodewidget(BoxLayout):
    def updating(self):
        TextWidget.text = ZBarCam.codedata
    def updating2(self):
        TextWidget.text2 = ZBarCam.codedata
    pass



DEMO_APP_KV_LANG = """
#:import ZBarSymbol pyzbar.pyzbar.ZBarSymbol
<qrcodewidget>:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
        code_types: ZBarSymbol.QRCODE, ZBarSymbol.EAN13
    Label:
        size_hint: None, None
        size: self.texture_size[0], 50
        text: ', '.join([str(symbol.data) for symbol in zbarcam.symbols])
    Button:
        text:"hash"
        font_size: 68
        on_press:root.updating()
        on_press:app.root.current="textwidget"
    Button:
        text:"address"
        font_size: 68
        on_press:root.updating2()
        on_press:app.root.current="textwidget"
        
"""

Builder.load_string(DEMO_APP_KV_LANG)





class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)

    def build(self):
        self.screen_manager = ScreenManager()

        self.text_widget = TextWidget()
        screen = Screen(name="textwidget")
        screen.add_widget(self.text_widget)
        self.screen_manager.add_widget(screen)

        self.camera_page = qrcodewidget()
        screen = Screen(name="qrpage")
        screen.add_widget(self.camera_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == '__main__':
    signapp=TestApp()
    signapp.run()