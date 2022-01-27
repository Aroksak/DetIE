# coding: utf-8
import hydra
from time import time
from tqdm import tqdm

from modules.model import models
from config.hydra import cleanup_hydra
from modules.model.apply import pprint_triplets
from torch.utils.data import DataLoader

TEST_TEXTS = ["This is how Agent Archer received a medal from the US.",
              "Alexander Pushkin was shot at a duel in St. Petersburg.",
              "The assault rifle is one of the very popular weapons in the Sahara desert.",
              "Bill Gates owns Microsoft Corporation.",
              "Lindon fictional universe where entity is from legendarium, The Boeing Company produces 747, "
              "population of Ukraine has census Ukrainian Census (2020), Bellecour is on Lyon Metro Line D, "
              "Vierwaldstättersee uses transport by boat, Wang Mang follows religion Confucianism.",
              "Фоллаут есть отличная постапокалиптическая игра",
              "Roses are red. Violets are blue. Cleaning automatic rifles is the only thing I ever do."
              ]


@cleanup_hydra
@hydra.main('../../config', 'config.yaml')
def main(cfg):
    model = getattr(models, cfg.model.name).load_from_checkpoint(
        checkpoint_path=cfg.model.best_ckpt_path,
        hparams_file=cfg.model.best_hparams_path
    ).cuda()
    # model.postprocess_adp = True
    # model.init_tools()
    # # texts = list(cfg.model.viz_sentences)
    # triplets = model.predict(list(cfg.model.viz_sentences))
    # pprint_triplets(TEST_TEXTS, triplets)

    BATCH_SIZE = 32
    with open('modules/model/evaluation/oie-benchmark-stanovsky/raw_sentences/all.txt') as f:
        sentences = f.readlines()

    start_time = time()
    loader = DataLoader(sentences, batch_size=BATCH_SIZE, collate_fn=lambda x: x, shuffle=False)
    for batch in tqdm(loader):
        preds = model.predict(batch)
    print(time() - start_time)


if __name__ == '__main__':
    main()

    # # for local tests
    # best_ckpt_path = "../../results/logs/default/version_158/checkpoints/best.ckpt"
    # best_hparams_path = "../../rresults/logs/default/version_158/hparams.yaml"
    # model = TripletsExtractor.load_from_checkpoint(checkpoint_path=best_ckpt_path, hparams_file=best_hparams_path)
    #
    # # texts = list(cfg.model.viz_sentences)
    # triplets = model.predict(TEST_TEXTS)
    # pprint_triplets(TEST_TEXTS, triplets)
