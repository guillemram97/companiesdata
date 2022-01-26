
fairseq-train $DATA_DIR --encoder-normalize-before --decoder-normalize-before --arch mbart_large --layernorm-embedding --task translation_from_pretrained_bart --source-lang tr_TR --target-lang en_XX --criterion cross_entropy --optimizer adam --adam-eps 1e-06 --adam-betas '(0.9, 0.98)' --lr-scheduler polynomial_decay --lr 3e-05 --dropout 0.3 --attention-dropout 0.1 --weight-decay 0.0 --warmup-updates 2500 --total-num-update 80000 --max-tokens $token_size  --update-freq 8 --langs $langs --no-epoch-checkpoints  --patience 5 --save-dir $SAVE_DIR --fp16 --restore-file $SAVE_DIR/checkpoint_best.pt
```





```
PRETRAIN=ckpts/tr-en/synthetic/edi/checkpoint_best.pt
DATA_DIR=data/bin/
SAVE_DIR=/guillem/prova
langs=ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN

token_size=1024

fairseq-train $DATA_DIR --encoder-normalize-before --decoder-normalize-before --arch mbart_large --layernorm-embedding --task translation_from_pretrained_bart --source-lang tr_TR --target-lang en_XX --criterion cross_entropy --optimizer adam --adam-eps 1e-06 --adam-betas '(0.9, 0.98)' --lr-scheduler polynomial_decay --lr 3e-05 --dropout 0.3 --attention-dropout 0.1 --weight-decay 0.0 --warmup-updates 2500 --total-num-update 80000 --max-tokens $token_size  --update-freq 8 --langs $langs --no-epoch-checkpoints  --patience 5 --save-dir $SAVE_DIR --fp16 --restore-file $SAVE_DIR/checkpoint_best.pt
```




Note that we did not use label-smoothing and use a few hparams different than the example. You can easily change this what works best for you. See the [fairseq documentation](https://fairseq.readthedocs.io/en/latest/command_line_tools.html). 

For finetuning, you might want to start with the already trained model which is available under `ckpts/tr-en/synthetic/edi/checkpoint_best.pt`. 


**en-tr**  
For the direction English into Turkish, we have a similar setup to `tr-en`; once again we use parallel data and a subsample of backtranslations. The subsample can be found under `data/backtranslations/edi/en-tr`. 
However, this time we train a multilingual model and pretend that the synthetic language is a language of its own. See for multilingual translation instructions [here](https://github.com/pytorch/fairseq/tree/main/examples/multilingual).  
The idea is that we use a language-token to identify synthetic inputs. Concretely, this means we initialise the 'synthetic-language' token with the embedding of the source-language token from the pretrained mBART25. In this case, for practical convenience we used the language token `NL_XX` as the synthetic language token and replaced its embeddings by the English embeddings(`EN_XX`). This requires a bit of different preprocessing step and could look like this:
```
DICT=mbart.cc25.v2/dict.txt
echo "Binarize the training setup for en-tr synthetic 'en' is now 'nl' "
fairseq-preprocess --source-lang nl_XX --target-lang tr_TR --trainpref data/BT-edi/train-en-tr-multi-synth/synthetic/train.bpe.tr-en \
  --validpref data/BT-edi/train-en-tr-multi-synth/synthetic/dev.bpe.tr-en --testpref data/BT-edi/train-en-tr-multi-synth/synthetic/devtest.bpe.tr-en \
  --destdir data/BT-edi/train-en-tr-multi-synth/bin/ --thresholdtgt 0 --thresholdsrc 0 --srcdict ${DICT} --tgtdict ${DICT}
echo "Done"

echo "Binarize the training setup en-tr original"
fairseq-preprocess --source-lang en_XX --target-lang tr_TR --trainpref data/train.bpe.tr-en --validpref data/dev.bpe.tr-en --testpref data/devtest.bpe.tr-en \
  --destdir data/BT-edi/train-en-tr-multi-synth/bin --thresholdtgt 0 --thresholdsrc 0 --srcdict ${DICT} --tgtdict data/BT-edi/train-en-tr-multi-synth/bin/dict.tr_TR.txt
echo "Done"
```
In addition, we need to copy and replace the `NL_XX` embeddings in the pretrained mBART25 model which can be found under `models/ln-token-mbart25/en-tr/mbart25-en-tr-adjusted.pt`

We can then train it like this for example:
```
PRETRAIN=mbart25-en-tr-adjusted.pt
DATA_DIR=data/BT-edi/train-en-tr-multi-synth/bin/
SAVE_DIR=/project/wilkgpu/lina/data-tr/ckpts/baseline/synthetic/multi/init/
token_size=1024
fairseq-train $DATA_DIR --encoder-normalize-before --decoder-normalize-before --arch mbart_large \
  --layernorm-embedding --task translation_multi_simple_epoch --lang-pairs en_XX-tr_TR,nl_XX-tr_TR  --lang-dict langs.file \
  --criterion cross_entropy --optimizer adam --adam-eps 1e-06 --adam-betas '(0.9, 0.98)' --lr-scheduler polynomial_decay --lr 3e-05 \
  --dropout 0.3 --attention-dropout 0.1 --weight-decay 0.0 --warmup-updates 2500 --total-num-update 80000 --max-tokens $token_size  \
  --update-freq 8 --finetune-from-model $PRETRAIN  --no-epoch-checkpoints  --patience 5 --save-dir $SAVE_DIR --fp16 \
  --sampling-method "temperature" --sampling-temperature 1.5 --encoder-langtok "src" 
```
Note that you need in this case a ``--lang-dict langs.file``, this is just a file containing the ids of the languages and can be found under `models/langs.file`. 

However, I think for finetuning with a specific goal, it might not be necessary to have this distinction. In that case, I think you can just process the data as usual (no need for a 'second language') and load in the already trained model which can be found under `ckpts/en-tr/synthetic/edi-ln-token/checkpoint_best.pt` (so I think you can replace the ``--finetune-from-model`` with an already trained model rather than mBART25).  


## Experiments and results
SacreBLEU results for different experiments. 

| System |  | en-tr |  |  |  | tr-en |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |
|  | dev | devtest | test |  | dev | devtest | test |
| Parallel | 20.6 | 22.2 | 18.7 |  | 26.5 | 26.8 | 27.1 |
| + Tatoeba wikinews | 21.2 | 22.8 | 19.3 |  | 28.7 | 28.1 | 29.0 |
| + Edinburgh NewsCrawl | 20.8 | 23.4 | 19.6 |  | 29.0 | 28.6 | 29.1 |
| Edinburgh NewsCrawl + synthetic language token | 22.0 | 24.3 | 20.2 |  | 28.6 | 28.7 | 29.0 |

| System | en-tr |  |  | tr-en |  |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  | BBC dev | BBC test |  | BBC dev | BBC test |
| + Tatoeba wikinews | 21.2 | 20.1 |  | 34.6 | 33.9 |
| + Edinburgh NewsCrawl | 20.3 | 20.3 |  | 34.7 | 33.9 |
| Edinburgh NewsCrawl + synthetic language token | 21.3 | 20.4 |  | 33.7 | 33.1 |
