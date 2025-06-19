import threading
import time
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
import numpy as np
from PIL import ImageGrab
import pyaudio
import wave
import ffmpeg
import os

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        image = Image(source='screen/PianoPicture.png', size_hint=(1, 0.8))
        layout.add_widget(image)
        start_button = Button(text="START", size_hint=(None, None), size=(300, 100), font_size='24sp', pos_hint={'center_x': 0.5})
        start_button.bind(on_press=self.start_piano)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def start_piano(self, instance):
        self.manager.current = 'piano'

class PianoScreen(Screen):
    def __init__(self, **kwargs):
        super(PianoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, padding=10, spacing=10)
        
        self.record_button = Button(text="Start Recording", size_hint=(None, None), size=(200, 50))
        self.record_button.bind(on_press=self.toggle_recording)
        top_layout.add_widget(self.record_button)
        
        self.open_video_folder_button = Button(text="Open Video Folder", size_hint=(None, None), size=(200, 50))
        self.open_video_folder_button.bind(on_press=self.open_video_folder)
        top_layout.add_widget(self.open_video_folder_button)
        
        self.open_notes_folder_button = Button(text="Open Notes Folder", size_hint=(None, None), size=(200, 50))
        self.open_notes_folder_button.bind(on_press=self.open_notes_folder)
        top_layout.add_widget(self.open_notes_folder_button)
        
        self.back_button = Button(text="Back", size_hint=(None, None), size=(200, 50))
        self.back_button.bind(on_press=self.go_back)
        top_layout.add_widget(self.back_button)
        
        layout.add_widget(top_layout)
        piano_layout = Piano()
        layout.add_widget(piano_layout)
        self.add_widget(layout)

    def toggle_recording(self, instance):
        self.children[1].toggle_recording(instance)

    def open_video_folder(self, instance):
        self.children[1].open_video_folder(instance)

    def open_notes_folder(self, instance):
        self.children[1].open_notes_folder(instance)

    def go_back(self, instance):
        self.manager.current = 'start'

class Piano(BoxLayout):
    button_a = ObjectProperty(None)
    button_s = ObjectProperty(None)
    button_d = ObjectProperty(None)
    button_f = ObjectProperty(None)
    button_g = ObjectProperty(None)
    button_h = ObjectProperty(None)
    button_j = ObjectProperty(None)
    button_k = ObjectProperty(None)
    button_l = ObjectProperty(None)
    button_ว = ObjectProperty(None)
    button_ง = ObjectProperty(None)
    button_enter = ObjectProperty(None)
    button_q = ObjectProperty(None)
    button_w = ObjectProperty(None)
    button_e = ObjectProperty(None)
    button_r = ObjectProperty(None)
    button_t = ObjectProperty(None)
    button_y = ObjectProperty(None)
    button_u = ObjectProperty(None)
    button_i = ObjectProperty(None)
    button_o = ObjectProperty(None)
    button_p = ObjectProperty(None)
    button_บ = ObjectProperty(None)
    button_ล = ObjectProperty(None)
    button_z = ObjectProperty(None)
    button_x = ObjectProperty(None)
    button_c = ObjectProperty(None)
    button_v = ObjectProperty(None)
    button_b = ObjectProperty(None)
    button_n = ObjectProperty(None)
    button_m = ObjectProperty(None)
    button_ม = ObjectProperty(None)
    button_ใ = ObjectProperty(None)
    button_ฝ = ObjectProperty(None)
    button_rshift = ObjectProperty(None)
    button_r1 = ObjectProperty(None)
    button_1 = ObjectProperty(None)
    button_2 = ObjectProperty(None)
    button_3 = ObjectProperty(None)
    button_4 = ObjectProperty(None)
    button_5 = ObjectProperty(None)
    button_6 = ObjectProperty(None)
    button_7 = ObjectProperty(None)
    button_8 = ObjectProperty(None)
    button_9 = ObjectProperty(None)
    button_0 = ObjectProperty(None)
    button_ข = ObjectProperty(None)
    button_ช = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        self.keys = {
            29: ("A1", self.button_z),
            54: ("A#1", self.button_ม),
            27: ("A2", self.button_x),
            55: ("A#2", self.button_ใ),
            6: ("A3", self.button_c),
            25: ("A4", self.button_v),
            56: ("A#4", self.button_ฝ),
            5: ("A5", self.button_b),
            229: ("A#5", self.button_rshift),
            17: ("A6", self.button_n),
            89: ("A#6", self.button_r1),
            16: ("A7", self.button_m),
            4: ("B1", self.button_a),
            14: ("B#1", self.button_k),
            22: ("B2", self.button_s),
            15: ("B#2", self.button_l),
            7: ("B3", self.button_d),
            9: ("B4", self.button_f),
            51: ("B#4", self.button_ว),
            10: ("B5", self.button_g),
            52: ("B#5", self.button_ง),
            11: ("B6", self.button_h),
            40: ("B#6", self.button_enter),
            13: ("B7", self.button_j),
            20: ("C1", self.button_q),
            12: ("C#1", self.button_i),
            26: ("C2", self.button_w),
            18: ("C#2", self.button_o),
            8: ("C3", self.button_e),
            21: ("C4", self.button_r),
            19: ("C#4", self.button_p),
            23: ("C5", self.button_t),
            47: ("C#5", self.button_บ),
            28: ("C6", self.button_y),
            48: ("C#6", self.button_ล),
            24: ("C7", self.button_u),
            30: ("D1", self.button_1),
            37: ("D#1", self.button_8),
            31: ("D2", self.button_2),
            38: ("D#2", self.button_9),
            32: ("D3", self.button_3),
            33: ("D4", self.button_4),
            39: ("D#4", self.button_0),
            34: ("D5", self.button_5),
            45: ("D#5", self.button_ข),
            35: ("D6", self.button_6),
            46: ("D#6", self.button_ช),
            36: ("D7", self.button_7),
        }

        self.sounds = {}
        sound_directory = './sounds/'
        for key, (note, _) in self.keys.items():
            sound = SoundLoader.load(f"./sounds/{note}.wav")
            if sound:
                sound.volume = 1.0
                self.sounds[key] = sound
            sound_file = os.path.join(sound_directory, f"{note}.wav")
            if os.path.exists(sound_file):
                sound = SoundLoader.load(sound_file)
                if sound:
                    sound.volume = 1.0
                    self.sounds[key] = sound
                else:
                    print(f"❌ Failed to load {note}.wav")
            else:
                print(f"❌ Failed to load {note}.wav")
                print(f"❌ {sound_file} does not exist.")

        self.pressed_keys = set()
        self.active_sounds = {}
        self.fade_threads = {}

        # Audio recording setup
        self.audio_frames = []
        self.audio_stream = None
        self.audio_thread = None

        # Create directories if they don't exist
        os.makedirs('video_recording', exist_ok=True)
        os.makedirs('recordings_note', exist_ok=True)
        self.notes_file = None

    def play_sound(self, key):
        if key in self.sounds:
            sound = self.sounds[key]
            if key in self.fade_threads:
                self.fade_threads[key] = False
                time.sleep(0.05)
            sound.seek(0)
            sound.volume = 1.0
            def play():
                sound.play()
                self.active_sounds[key] = sound
            threading.Thread(target=play, daemon=True).start()

    def fade_out(self, key):
        if key in self.active_sounds:
            sound = self.active_sounds[key]
            self.fade_threads[key] = True
            while sound.volume > 0 and self.fade_threads[key]:
                sound.volume = max(0, sound.volume - 0.02)
                time.sleep(0.05)
            if self.fade_threads[key]:
                sound.stop()
                del self.active_sounds[key]
            del self.fade_threads[key]

    def on_key_down(self, instance, keycode, keyname, *args):
        for key, (note, button) in self.keys.items():
            if keycode[1] == keyname:
                if key not in self.pressed_keys:
                    self.pressed_keys.add(key)
                    threading.Thread(target=self.play_sound, args=(key,), daemon=True).start()
                    if self.notes_file:
                        self.notes_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {note}\n")
                        self.notes_file.flush()
                if button:
                    button.state = 'down'

    def on_key_up(self, instance, keycode, keyname, *args):
        for key, (note, button) in self.keys.items():
            if keycode[1] == keyname:
                if key in self.active_sounds:
                    fade_thread = threading.Thread(target=self.fade_out, args=(key,))
                    fade_thread.start()
                if key in self.pressed_keys:
                    self.pressed_keys.remove(key)
                if button:
                    button.state = 'normal'

    def toggle_recording(self, instance):
        if self.recording:
            self.record_button.text = "Start Recording"
            self.recording = False
            self.out.release()
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            if self.out:
                self.out.release()
            if self.audio_stream:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            self.audio_thread.join()
            self.save_audio()
            self.merge_audio_video()
            if self.notes_file:
                self.notes_file.close()
        else:
            self.record_button.text = "Stop Recording"
            self.recording = True
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.video_filename = f'video_recording/output_{timestamp}.avi'
            self.audio_filename = f'video_recording/output_{timestamp}.wav'
            self.output_filename = f'video_recording/output_with_audio_{timestamp}.avi'
            self.notes_filename = f'recordings_note/notes_{timestamp}.txt'
            self.notes_file = open(self.notes_filename, 'a')
            self.out = cv2.VideoWriter(self.video_filename, cv2.VideoWriter_fourcc(*'XVID'), 8.0, (Window.width, Window.height))
            Clock.schedule_interval(self.record_frame, 1 / 8)
            self.start_audio_recording()

    def record_frame(self, dt):
        if self.recording:
            img = ImageGrab.grab(bbox=(Window.left, Window.top, Window.left + Window.width, Window.top + Window.height))
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            self.out.write(frame)

    def start_audio_recording(self):
        self.audio_frames = []
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.audio_thread.start()
        try:
            self.audio_thread.start()
        except Exception as e:
            print(f"❌ Failed to start audio recording: {e}")

    def record_audio(self):
        p = pyaudio.PyAudio()
        self.audio_stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
        while self.recording:
            data = self.audio_stream.read(1024)
            self.audio_frames.append(data)
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        p.terminate()
        try:
            p = pyaudio.PyAudio()
            self.audio_stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
            while self.recording:
                data = self.audio_stream.read(1024)
                self.audio_frames.append(data)
        except Exception as e:
            print(f"❌ Error in recording audio: {e}")
        finally:
            if hasattr(self, 'audio_stream'):
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            if 'p' in locals():
                p.terminate()

    def save_audio(self):
        wf = wave.open(self.audio_filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.audio_frames))
        wf.close()

    def merge_audio_video(self):
        input_video = ffmpeg.input(self.video_filename)
        input_audio = ffmpeg.input(self.audio_filename)
        ffmpeg.output(input_video, input_audio, self.output_filename, vcodec='copy', acodec='aac', strict='experimental').run()
        try:
            input_video = ffmpeg.input(self.video_filename)
            input_audio = ffmpeg.input(self.audio_filename)
            ffmpeg.output(input_video, input_audio, self.output_filename, vcodec='copy', acodec='aac', strict='experimental').run()
        except Exception as e:
            print(f"❌ Error in merging audio and video: {e}")

    def open_video_folder(self, instance):
        os.startfile(os.path.abspath('video_recording'))

    def open_notes_folder(self, instance):
        os.startfile(os.path.abspath('recordings_note'))

class PianoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(PianoScreen(name='piano'))
        return sm

if __name__ == '__main__':
    PianoApp().run()

