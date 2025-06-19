import threading
import time
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.clock import Clock
import cv2
import numpy as np
from PIL import ImageGrab
import pyaudio
import wave
import ffmpeg
import os

class Piano(BoxLayout):
    button_1 = ObjectProperty(None)
    button_2 = ObjectProperty(None)
    button_3 = ObjectProperty(None)
    button_4 = ObjectProperty(None)
    button_5 = ObjectProperty(None)
    button_6 = ObjectProperty(None)
    button_7 = ObjectProperty(None)
    button_a = ObjectProperty(None)
    button_s = ObjectProperty(None)
    button_d = ObjectProperty(None)
    button_f = ObjectProperty(None)
    button_g = ObjectProperty(None)
    button_h = ObjectProperty(None)
    button_j = ObjectProperty(None)
    button_q = ObjectProperty(None)
    button_w = ObjectProperty(None)
    button_e = ObjectProperty(None)
    button_r = ObjectProperty(None)
    button_t = ObjectProperty(None)
    button_y = ObjectProperty(None)
    button_u = ObjectProperty(None)
    button_z = ObjectProperty(None)
    button_x = ObjectProperty(None)
    button_c = ObjectProperty(None)
    button_v = ObjectProperty(None)
    button_b = ObjectProperty(None)
    button_n = ObjectProperty(None)
    button_m = ObjectProperty(None)
    button_shift_z = ObjectProperty(None)
    button_shift_x = ObjectProperty(None)
    button_shift_v = ObjectProperty(None)
    button_shift_b = ObjectProperty(None)
    button_shift_n = ObjectProperty(None)
    button_shift_a = ObjectProperty(None)
    button_shift_s = ObjectProperty(None)
    button_shift_f = ObjectProperty(None)
    button_shift_g = ObjectProperty(None)
    button_shift_h = ObjectProperty(None)
    button_shift_q = ObjectProperty(None)
    button_shift_w = ObjectProperty(None)
    button_shift_r = ObjectProperty(None)
    button_shift_t = ObjectProperty(None)
    button_shift_y = ObjectProperty(None)
    button_shift_1 = ObjectProperty(None)
    button_shift_2 = ObjectProperty(None)
    button_shift_4 = ObjectProperty(None)
    button_shift_5 = ObjectProperty(None)
    button_shift_6 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        # กำหนดปุ่มกับโน้ตดนตรี
        self.keys = {
            122: ("A1", self.button_z),  # z
            (122, 'shift'): ("A#1", self.button_shift_z),
            120: ("A2", self.button_x),  # x
            (120, 'shift'): ("A#2", self.button_shift_x),
            99: ("A3", self.button_c),  # c
            118: ("A4", self.button_v),  # v
            (118, 'shift'): ("A#4", self.button_shift_v),
            98: ("A5", self.button_b),  # b
            (98, 'shift'): ("A#5", self.button_shift_b),
            110: ("A6", self.button_n),  # n
            (110, 'shift'): ("A#6", self.button_shift_n),
            109: ("A7", self.button_m),  # m
            97: ("B1", self.button_a),  # a
            (97, 'shift'): ("B#1", self.button_shift_a),
            115: ("B2", self.button_s),  # s
            (115, 'shift'): ("B#2", self.button_shift_s),
            100: ("B3", self.button_d),  # d
            102: ("B4", self.button_f),  # f
            (102, 'shift'): ("B#4", self.button_shift_f),
            103: ("B5", self.button_g),  # g
            (103, 'shift'): ("B#5", self.button_shift_g),
            104: ("B6", self.button_h),  # h
            (104, 'shift'): ("B#6", self.button_shift_h),
            106: ("B7", self.button_j),  # j
            113: ("C1", self.button_q),  # q
            (113, 'shift'): ("C#1", self.button_shift_q),
            119: ("C2", self.button_w),  # w
            (119, 'shift'): ("C#2", self.button_shift_w),
            101: ("C3", self.button_e),  # e
            114: ("C4", self.button_r),  # r
            (114, 'shift'): ("C#4", self.button_shift_r),
            116: ("C5", self.button_t),  # t
            (116, 'shift'): ("C#5", self.button_shift_t),
            121: ("C6", self.button_y),  # y
            (121, 'shift'): ("C#6", self.button_shift_y),
            117: ("C7", self.button_u),  # u
            49: ("D1", self.button_1),  # 1
            (49, 'shift'): ("D#1", self.button_shift_1),
            50: ("D2", self.button_2),  # 2
            (50, 'shift'): ("D#2", self.button_shift_2),
            51: ("D3", self.button_3),  # 3
            52: ("D4", self.button_4),  # 4
            (52, 'shift'): ("D#4", self.button_shift_4),
            53: ("D5", self.button_5),  # 5
            (53, 'shift'): ("D#5", self.button_shift_5),
            54: ("D6", self.button_6),  # 6
            (54, 'shift'): ("D#6", self.button_shift_6),
            55: ("D7", self.button_7),  # 7
        }

        # โหลดไฟล์เสียงล่วงหน้า
        self.sounds = {}
        for key, (note, _) in self.keys.items():
            sound = SoundLoader.load(f"./sounds/{note}.wav")
            if sound:
                sound.volume = 1.0
                self.sounds[key] = sound
            else:
                print(f"❌ Failed to load {note}.wav")

        # เก็บสถานะปุ่มที่กดอยู่
        self.pressed_keys = set()

        # เก็บเสียงที่กำลังเล่น และ Thread ที่ใช้ลดเสียง
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

        # Initialize recording state
        self.recording = False

    def play_sound(self, key):
        """ เล่นเสียงเมื่อกดปุ่ม """
        if key in self.sounds:
            sound = self.sounds[key]
            print(f"Playing sound: {sound.source}")

            # ถ้ากำลังลดเสียงอยู่ให้ยกเลิกก่อน
            if key in self.fade_threads:
                self.fade_threads[key] = False  # บอก Thread ว่าให้หยุดลดเสียงก่อน
                time.sleep(0.05)  # รอให้ Thread ปิดตัวลงก่อนเล่นเสียงใหม่

            sound.seek(0)  # รีเซ็ตเสียงเพื่อให้เล่นตั้งแต่ต้น
            sound.volume = 1.0  # ตั้งค่าเสียงให้เต็ม

            # สร้าง Thread เพื่อเล่นเสียง
            def play():
                sound.play()
                self.active_sounds[key] = sound  # เก็บเสียงที่กำลังเล่นอยู่

            threading.Thread(target=play, daemon=True).start()

    def fade_out(self, key):
        """ ลดเสียงลงเรื่อยๆ จนเงียบ แล้วหยุดเสียง """
        if key in self.active_sounds:
            sound = self.active_sounds[key]
            self.fade_threads[key] = True  # เปิดใช้งาน Thread ลดเสียง

            while sound.volume > 0 and self.fade_threads.get(key, False):  # ลดเสียงเฉพาะถ้าไม่ได้ถูกยกเลิก
                sound.volume = max(0, sound.volume - 0.02)  # ค่อยๆ ลดเสียงลง
                time.sleep(0.05)  # ลดเสียงทีละ 0.05 วินาที

            if self.fade_threads.get(key, False):  # ถ้า Thread ไม่ถูกยกเลิกให้หยุดเสียง
                sound.stop()
                del self.active_sounds[key]

            self.fade_threads.pop(key, None)  # ลบ Thread ออกจากรายการ

    def on_key_down(self, instance, keycode, keyname, text, modifiers):
        """ กดปุ่มแล้วเล่นเสียง (ใช้ Thread) """
        key = keycode
        if 'shift' in modifiers:
            key = (keycode, 'shift')
        print(key)
        if key in self.keys:
            note, button = self.keys[key]
            if key not in self.pressed_keys:
                self.pressed_keys.add(key)
                threading.Thread(target=self.play_sound, args=(key,), daemon=True).start()
            if button:
                button.state = 'down'
            if self.notes_file:
                self.notes_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {note}\n")

    def on_key_up(self, instance, keycode, keyname):
        """ เมื่อปล่อยปุ่มให้ลดเสียงลงเรื่อยๆ """
        key = keycode
        if 'shift' in Window.modifiers:
            key = (keycode, 'shift')
        if key in self.keys:
            note, button = self.keys[key]
            if key in self.active_sounds:
                fade_thread = threading.Thread(target=self.fade_out, args=(key,))
                fade_thread.start()
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
            if button:
                button.state = 'normal'

    def toggle_recording(self, instance):
        if self.recording:
            instance.text = "Start Recording"
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
            instance.text = "Stop Recording"
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
        return Piano()

if __name__ == '__main__':
    PianoApp().run()