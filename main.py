from utils.HTU21D_logger import HTU21DLogger

if __name__ == "__main__":
    logger = HTU21DLogger("./config.json", "./secrets.json")
    logger.run()
