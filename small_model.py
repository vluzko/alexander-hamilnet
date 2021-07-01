from pathlib import Path
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling


DATA = Path(__file__).parent / 'data'


def load_dataset(train_path, test_path, tokenizer):
    train_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=train_path,
          block_size=128)

    test_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=test_path,
          block_size=128)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset,test_dataset,data_collator


def main():
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    train_path = DATA / 'train_fed.txt'
    test_path = DATA / 'test_fed.txt'

    train_dataset, test_dataset, data_collator = load_dataset(str(train_path), str(test_path), tokenizer)

    training_args = TrainingArguments(
        output_dir="./data/gpt2",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=64,
        eval_steps = 400,
        save_steps=800,
        warmup_steps=500
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset
    )
    trainer.train()


if __name__ == '__main__':
    main()
