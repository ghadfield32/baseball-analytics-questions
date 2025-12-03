# Q2 – Model serving: batched inference API with timeouts

# You’re serving an xG-style model that takes fixed-length feature vectors for shots and returns a probability. You want to batch requests for GPU efficiency, but you also need latency under 100ms per request.

# Design a simple Python API layer (no need for full FastAPI boilerplate) that:

# Accepts individual prediction requests from multiple threads.

# Batches them into tensors of size up to 128.

# Ensures no request waits longer than 50ms in the queue before being run.

# Show:

# How you’d structure the worker thread / queue.

# A predict(features) function that a caller would use.

# How you’d handle shutdown cleanly.

# (This is exactly the kind of “bridge between Baseball Analytics models and Baseball Systems tools” they care about.)



import time
from queue import Empty, Queue
from threading import Event, Thread


class PredictionRequest:
    def __init__(self, features):
        self.features = features
        self.event = Event()
        self.result = None

class BatchedPredictor:
    def __init__(self, model, max_batch_size=128, max_wait_ms=50):
        self.model = model
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.queue = Queue()
        self._stop = Event()
        self.worker = Thread(target=self._batch_worker, daemon=True)
        self.worker.start()

    def predict(self, features):
        req = PredictionRequest(features)
        self.queue.put(req)
        req.event.wait()
        return req.result

    def _batch_worker(self):
        while not self._stop.is_set():
            batch = []
            batch_start = time.time()
            try:
                req = self.queue.get(timeout=0.05)
                batch.append(req)
                while len(batch) < self.max_batch_size:
                    wait_time = self.max_wait_ms / 1000 - (time.time() - batch_start)
                    if wait_time <= 0:
                        break
                    try:
                        req = self.queue.get(timeout=wait_time)
                        batch.append(req)
                    except Empty:
                        break
            except Empty:
                continue

            if batch:
                features_batch = [r.features for r in batch]
                preds = self.model.predict(features_batch)
                for req, pred in zip(batch, preds):
                    req.result = pred
                    req.event.set()

    def shutdown(self):
        self._stop.set()
        self.worker.join()


# Smoke test: simple dummy model
class DummyModel:
    def predict(self, batch):
        return [sum(f) for f in batch]

if __name__ == "__main__":
    import threading

    scorer = BatchedPredictor(DummyModel(), max_batch_size=4, max_wait_ms=20)

    results = []
    def worker(i):
        out = scorer.predict([i, i+1, i+2])
        results.append((i, out))

    # Happy path: less than batch size
    t1 = threading.Thread(target=worker, args=(1,))
    t2 = threading.Thread(target=worker, args=(7,))
    t1.start(); t2.start(); t1.join(); t2.join()
    print("Happy path:", results)

    # Edge: lots of requests, check batching and no more than batch size per batch
    results.clear()
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Stress test:", results)

    scorer.shutdown()


