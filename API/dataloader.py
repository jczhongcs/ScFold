import copy
import os.path as osp

from API.cath_dataset import CATH
from API.ts_dataset import TS

from API.dataloader_gtrans import DataLoader_GTrans
from API.featurizer import featurize_GTrans


def load_data(data_name, method, batch_size, data_root, num_workers=8, **kwargs):
    if data_name == 'CATH' or data_name == 'TS50'or data_name == 'TS500':
        cath_set = CATH(osp.join(data_root, 'cath'), mode='train', test_name='All')
        train_set, valid_set, test_set = map(lambda x: copy.copy(x), [cath_set] * 3)

        valid_set.change_mode('valid')
        test_set.change_mode('test')
        if data_name == 'TS50':
            train_set = TS(osp.join(data_root, 'ts50.json'))
            valid_set = TS(osp.join(data_root, 'ts50.json'))
            test_set = TS(osp.join(data_root, 'ts50.json'))
        if data_name == 'TS500':
            train_set = TS(osp.join(data_root, 'ts500_300.json'))
            valid_set = TS(osp.join(data_root, 'ts500_300.json'))
            test_set = TS(osp.join(data_root, 'ts500_300.json'))
        collate_fn = featurize_GTrans

    train_loader = DataLoader_GTrans(train_set, batch_size=batch_size, shuffle=True, num_workers=num_workers,
                                     collate_fn=collate_fn)
    valid_loader = DataLoader_GTrans(valid_set, batch_size=batch_size, shuffle=False, num_workers=num_workers,
                                     collate_fn=collate_fn)
    test_loader = DataLoader_GTrans(test_set, batch_size=batch_size, shuffle=False, num_workers=num_workers,
                                    collate_fn=collate_fn)

    return train_loader, valid_loader, test_loader


def make_cath_loader(test_set, method, batch_size, max_nodes=3000, num_workers=8):
    collate_fn = featurize_GTrans
    test_loader = DataLoader_GTrans(test_set, batch_size=batch_size, shuffle=False, num_workers=num_workers,
                                    collate_fn=collate_fn)

    return test_loader