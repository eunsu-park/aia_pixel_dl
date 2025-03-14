import argparse


class Options:
    def __init__(self) :
        self.parser = argparse.ArgumentParser()

        # Options for all phases
        self.parser.add_argument("--seed", type=int,
                                 default=250104, help="random seed")
        self.parser.add_argument("--device", type=str,
                                 default="cuda", help="device")
        self.parser.add_argument("--phase", type=str,
                                 choices=["train", "test", "clustering"],
                                 help="phase")
        self.parser.add_argument("--data_root", type=str,
                                 help="data root directory")
        self.parser.add_argument("--save_root", type=str,
                                 help="save directory")
        self.parser.add_argument("--batch_size", type=int,
                                 default=1, help="batch size")
        self.parser.add_argument("--num_workers", type=int,
                                 default=4, help="number of workers")
        self.parser.add_argument("--experiment_name", type=str,
                                 help="experiment name")        
        self.parser.add_argument("--network_type", type=str,
                                 choices=["autoencoder", "variational_autoencoder"],
                                 default="autoencoder", help="network type")
        self.parser.add_argument("--layer_type", type=str,
                                 choices=["pixel", "conv"],
                                 default="pixel", help="layer type")
        self.parser.add_argument("--waves", type=int, nargs="+",
                                 default=[94, 131, 171, 193, 211, 335],
                                 help="wavelengths")
        self.parser.add_argument("--num_latent_features", type=int,
                                 default=50, help="number of latent features")
        self.parser.add_argument("--num_hidden_features", type=int,
                                 default=50, help="number of latent features")
        self.parser.add_argument("--init_type", type=str,
                                 choices=["normal", "xavier", "kaiming", "orthogonal"],
                                 default="normal", help="initialization type")
        self.parser.add_argument("--model_path", type=str,
                                 default="", help="model path")

        # Options for training
        self.parser.add_argument("--metric_type", type=str,
                                 choices=["mse", "mae", "log_cosh"],
                                 default="mae", help="metric function")
        self.parser.add_argument("--lr", type=float,
                                 default=0.0002, help="learning rate")
        self.parser.add_argument("--beta1", type=float,
                                 default=0.5, help="beta1 parameter of Adam optimizer")
        self.parser.add_argument("--beta2", type=float,
                                 default=0.999, help="beta2 parameter of Adam optimizer")
        self.parser.add_argument("--n_epochs", type=int,
                                 default=100, help="number of epochs")
        self.parser.add_argument("--report_freq", type=int,
                                 default=1000, help="report frequency in iterations")
        self.parser.add_argument("--save_freq", type=int,
                                 default=1, help="save frequency in epochs")

    def parse(self):
        args = self.parser.parse_args()
        args.num_euv_channels = len(args.waves)
        # self.parser.add_argument("--num_euv_channels", type=int,
        #                          default=6, help="number of EUV channels")
        # return self.parser.parse_args()
        return args
