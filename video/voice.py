import os

import torch
import soundfile as sf

from chatterbox.mtl_tts import ChatterboxMultilingualTTS


class VoiceGenerator:

    def __init__(
        self,
        voice_reference="data/voice_reference.wav"
    ):

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.voice_reference = voice_reference

        print(
            f"[VOICE] Device : {self.device}"
        )

        if self.device == "cuda":

            print(
                "[VOICE] GPU : "
                + torch.cuda.get_device_name(0)
            )

        print(
            "[VOICE] Chargement de Chatterbox..."
        )

        self.model = (
            ChatterboxMultilingualTTS
            .from_pretrained(
                device=self.device
            )
        )

        print(
            "[VOICE] Chatterbox chargé."
        )

    def generate(
        self,
        text,
        output_path,
        language="fr"
    ):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        print(
            "[VOICE] Génération de la voix..."
        )

        # IMPORTANT :
        # text doit être une chaîne de caractères.
        text = str(text)

        wav = self.model.generate(
            text,
            language_id=language,
            audio_prompt_path=self.voice_reference
        )

        audio = (
            wav
            .squeeze(0)
            .detach()
            .cpu()
            .numpy()
        )

        sf.write(
            output_path,
            audio,
            self.model.sr
        )

        duration = (
            len(audio)
            / self.model.sr
        )

        print(
            f"[VOICE] Audio créé : "
            f"{output_path}"
        )

        print(
            f"[VOICE] Durée : "
            f"{duration:.2f}s"
        )

        return {
            "path": output_path,
            "duration": duration,
            "sample_rate": self.model.sr
        }