import re
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, BitsAndBytesConfig

MODEL_NAME = "IlyaGusev/saiga_mistral_7b"
DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>"
DEFAULT_RESPONSE_TEMPLATE = "<s>bot\n"
DEFAULT_SYSTEM_PROMPT = "Ты — русскоязычный ассистент специалиста подбора персонала. Отвечаешь исключительно на русском языке. Ты помогаешь анализировать вакансии, извлекать из вакансий список требований и навыков. Ты не используешь информацию которой нет в тексте вакансий."
TEXT2SKILLS_MESSAGE = "Составь нумерованный список технологий которыми требуется владеть для данной вакансии. Текст вакансии: "


class Conversation:
    def __init__(
        self,
        message_template=DEFAULT_MESSAGE_TEMPLATE,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        response_template=DEFAULT_RESPONSE_TEMPLATE
    ):
        self.message_template = message_template
        self.response_template = response_template
        self.messages = [{
            "role": "system",
            "content": system_prompt
        }]

    def add_user_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_bot_message(self, message):
        self.messages.append({
            "role": "bot",
            "content": message
        })

    def get_prompt(self, tokenizer):
        final_text = ""
        for message in self.messages:
            message_text = self.message_template.format(**message)
            final_text += message_text
        final_text += DEFAULT_RESPONSE_TEMPLATE
        return final_text.strip()


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class SaigaHR:
    def __init__(self):
        config = PeftConfig.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            config.base_model_name_or_path,
            quantization_config=BitsAndBytesConfig(load_in_4bit=True),
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        model = PeftModel.from_pretrained(
            model,
            MODEL_NAME,
            torch_dtype=torch.bfloat16
        )
        model.eval()

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
        generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
        generation_config.repetition_penalty = 1.1
        generation_config.temperature = 0.02
        generation_config.max_new_tokens = 375
        generation_config.top_p = 0.90
        generation_config.top_k = 40

        self.tokenizer = tokenizer
        self.model = model
        self.generation_config = generation_config

    def vacancy_to_skills(self, extended_description):
        # construct prompt
        conversation = Conversation()
        conversation.add_user_message(TEXT2SKILLS_MESSAGE + re.sub(r'<.*?>', '', extended_description))
        prompt = conversation.get_prompt(self.tokenizer)
        # generate
        data = self.tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
        data = {k: v.to(self.model.device) for k, v in data.items()}
        output_ids = self.model.generate(
            **data,
            generation_config=self.generation_config
        )[0]
        output_ids = output_ids[len(data["input_ids"][0]):]
        output = self.tokenizer.decode(output_ids, skip_special_tokens=True)
        return output.strip()
