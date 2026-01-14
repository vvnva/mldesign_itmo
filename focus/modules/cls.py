
import json

from loguru import logger
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification as AMFSC,
)


def read_json(filepath: str, encoding: str = 'utf-8') -> dict:
    with open(filepath, 'r', encoding=encoding) as json_file:
        data = json.load(json_file)
    return data


class ClsBase:
    def __init__(
        self,
        tokenizer_path: str,
        models_paths: dict[str, dict[str, str]],
        device: str,
    ):
        self.tokenizer_path = tokenizer_path
        self.models_paths = models_paths
        self.device = device
        self._init_pipe()

    def _init_pipe(self):
        # structures
        self.pipe_models = {}
        pipe_labels = {}
        pipe_id2labels = {}
        self.cls_pipes = {}
        # models
        logger.warning(f"tokenizer: {self.tokenizer_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
        for lvl, paths in self.models_paths.items():
            logger.warning(f'{lvl}: {paths["model"]}')
            # Labels
            pipe_labels[lvl] = read_json(paths["labels"])
            pipe_id2labels[lvl] = {id: lbl for lbl, id in pipe_labels[lvl].items()}
            # Models
            self.pipe_models[lvl] = AMFSC.from_pretrained(paths["model"])
            self.pipe_models[lvl].config.label2id = pipe_labels[lvl]
            self.pipe_models[lvl].config.id2label = pipe_id2labels[lvl]
            self.pipe_models[lvl].eval()
            # Pipes
            self.cls_pipes[lvl] = pipeline(
                "text-classification",
                model=self.pipe_models[lvl],
                tokenizer=self.tokenizer,
                device=self.device,
            )


class TopicClsPipe(ClsBase):
    def inf(self, text: str) -> tuple[str, float]:
        # Top Topic (Binary)
        inf_res = self.cls_pipes["top-binary"](text)[0]
        if inf_res["label"] == "Остальное":
            # Low Topic (Rest)
            inf_res = self.cls_pipes["low-rest"](text)[0]
        res_top, res_prob = inf_res["label"], inf_res["score"]
        return res_top, res_prob


class SubtopicClsPipe(ClsBase):
    def inf(self, topic: str, text: str) -> tuple[str, float]:
        inf_res = self.cls_pipes[topic](text)[0]
        res_top, res_prob = inf_res["label"], inf_res["score"]
        res_top_f = "_".join(res_top.split("_")[1:])
        return res_top_f, res_prob


class Cls:
    def __init__(
            self,
            topt_tokenizer_path: str,
            topt_models_path: dict[str, dict[str, str]],
            subt_tokenizer_path: str,
            subt_models_path: dict[str, dict[str, str]],
            device: str,
        ):
        # topic
        self.topt_tokenizer_path = topt_tokenizer_path
        self.topt_models_path = topt_models_path
        # subtopic
        self.subt_tokenizer_path = subt_tokenizer_path
        self.subt_models_path = subt_models_path
        # rest
        self.device = device
        self._init_pipe()

    def _init_pipe(self):
        # topic
        self.topic_pipe = TopicClsPipe(
            self.topt_tokenizer_path,
            self.topt_models_path,
            self.device,
        )
        # subtopic
        self.subtopic_pipe = SubtopicClsPipe(
            self.subt_tokenizer_path,
            self.subt_models_path,
            self.device,
        )

    def inf(self, text: str) -> tuple[str, str]:
        top_name, top_p = self.topic_pipe.inf(text)
        sub_name, sub_p = self.subtopic_pipe.inf(top_name, text)
        return top_name, sub_name
