from datasets import Dataset
from transformers import MarianTokenizer, MarianMTModel, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
import pandas as pd

# Carregar dados
df = pd.read_csv("dados/pares_tr_pt.csv")
dataset = Dataset.from_pandas(df)

# Modelo base
model_name = "Helsinki-NLP/opus-mt-tr-pt"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Função para tokenização
def preprocess_function(examples):
    inputs = [ex["tr"] for ex in examples["translation"]]
    targets = [ex["pt"] for ex in examples["translation"]]
    model_inputs = tokenizer(inputs, max_length=128, truncation=True)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=128, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(preprocess_function, batched=True, remove_columns=["translation"])

# Configuração do treino
training_args = Seq2SeqTrainingArguments(
    output_dir="meu_tradutor_turco_pt",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=5,
    predict_with_generate=True,
    fp16=False  # Coloque True se tiver GPU com suporte
)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Treinar
trainer.train()

# Salvar modelo final
model.save_pretrained("meu_tradutor_turco_pt")
tokenizer.save_pretrained("meu_tradutor_turco_pt")
print("✅ Modelo treinado salvo em 'meu_tradutor_turco_pt'")
