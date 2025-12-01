import time

from load_model import *
from samples import *

class PromptKiller:
    def __init__(self, verbose=True):
        time_s = time.time()
        if verbose:
            print("[PromptKiller] Loading tokenizer...")
        self.tokenizer = get_tokenizer()

        if verbose:
            print("[PromptKiller] Loading model weights...")
        self.model = get_model()

        if verbose:
            print("[PromptKiller] Loading samples...")
        self.sman = SamplesManager()

        if verbose:
            print("[PromptKiller] Preparing sample features...")
        self.sman.embed_samples(self.embed_text)

        if verbose:
            time_e = time.time()
            print(f"[PromptKiller] Initialization complete in {(time_e - time_s):.2f} seconds.")
            print(f"[PromptKiller] Model running on device: {DEVICE}")

    def embed_text(self, text):
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt",
        )
        with torch.no_grad():
            features = self.model(
                input_ids=inputs["input_ids"],
                token_type_ids=inputs.get("token_type_ids", None),
                attention_mask=inputs["attention_mask"],
            )
        return features
    

    def predict(self, text, verbose=True):
        time_s = time.time()
        features = self.embed_text(text)

        sim_b_avg, sim_m_avg, text_sim = self.sman.get_similarities(features)

        sim_b = max(sim_b_avg)
        sim_m = max(sim_m_avg)
        res = 0 if sim_b >= sim_m else 1
        text_res = ["Benign", "Malicious"][res]

        time_e = time.time()
        if verbose:
            print(f"[PromptKiller] Prediction completed in {(time_e - time_s):.2f} seconds.")
            print(f"* {text_sim}")
            print(f"* Input Prompt:\t{text}")
            print(f"* Predicted:\t'{text_res}'")

        return res