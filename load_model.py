import torch
from transformers import AutoTokenizer, AutoModel
from peft import get_peft_model, LoraConfig, LoftQConfig

DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
PRETRAINED_MODEL = "microsoft/deberta-base"
FINETUNE_MODEL_PATH = "./weights/deberta_siamese.pth"

# Siamese BERT model for few-shot prompt classification
class SiameseBERTModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.pretrained_model = AutoModel.from_pretrained(PRETRAINED_MODEL)
        self.pretrained_model.to("cpu")

        # set PEFT
        loftq_config = LoftQConfig(loftq_bits=4)           # set 4bit quantization
        lora_config = LoraConfig(init_lora_weights="loftq", loftq_config=loftq_config, inference_mode=True)
        self.pretrained_model = get_peft_model(self.pretrained_model, lora_config)

        self.feature_head = torch.nn.Sequential(
            torch.nn.Linear(self.pretrained_model.config.hidden_size, 384),
        )

    def forward(self, input_ids, token_type_ids, attention_mask):
        input_ids = input_ids.to(DEVICE, non_blocking=True)
        attention_mask = attention_mask.to(DEVICE, non_blocking=True)

        outputs = self.pretrained_model(input_ids=input_ids, attention_mask=attention_mask)
        # Use the pooled output or last hidden state
        pooled_output = outputs.last_hidden_state[:, 0, :]
        return self.feature_head(pooled_output)

def get_tokenizer():
    return AutoTokenizer.from_pretrained(PRETRAINED_MODEL)

def get_model():
    model = SiameseBERTModel()
    model.load_state_dict(torch.load(FINETUNE_MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model