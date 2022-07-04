import torch
from sample_factory.algorithms.appo.model_utils import EncoderBase
from sample_factory.algorithms.appo.model_utils import register_custom_encoder
from transformers import RobertaConfig
from transformers import RobertaModel


class NLELanguageTransformerEncoder(EncoderBase):
    def __init__(self, cfg, obs_space, timing):
        super().__init__(cfg, timing)
        config = RobertaConfig(
            attention_probs_dropout_prob=0.0,
            bos_token_id=0,
            classifier_dropout=None,
            eos_token_id=2,
            hidden_act="gelu",
            hidden_dropout_prob=0.0,
            hidden_size=cfg.transformer_hidden_size,
            initializer_range=0.02,
            intermediate_size=cfg.transformer_hidden_size,
            layer_norm_eps=1e-05,
            max_position_embeddings=obs_space.spaces["input_ids"].shape[0]
            + 2,  # Roberta requires max sequence length + 2.
            model_type="roberta",
            num_attention_heads=cfg.transformer_attention_heads,
            num_hidden_layers=cfg.transformer_hidden_layers,
            pad_token_id=1,
            position_embedding_type="absolute",
            transformers_version="4.17.0",
            type_vocab_size=1,
            use_cache=False,
            vocab_size=50265,
        )
        self.model = RobertaModel(config=config)
        self.encoder_out_size = self.model.config.hidden_size

    def device_and_type_for_input_tensor(
        self, input_tensor_name
    ):  # pylint: disable=['unused-argument']
        return "cuda", torch.int32  # pylint: disable=['no-member']

    def forward(self, obs_dict):
        input_ids = obs_dict["input_ids"]
        attention_mask = obs_dict["attention_mask"]
        # Input transformation to allow for sample factory enjoy
        if len(input_ids.shape) == 3:
            input_ids = input_ids.squeeze(0)
            attention_mask = attention_mask.squeeze(0)
        if input_ids.dtype == torch.float32:  # pylint: disable=['no-member']
            input_ids = input_ids.long()
            attention_mask = attention_mask.long()
        output = self.model(input_ids=input_ids, attention_mask=attention_mask)
        return output.last_hidden_state[:, 0]


register_custom_encoder(
    "nle_language_transformer_encoder", NLELanguageTransformerEncoder
)
