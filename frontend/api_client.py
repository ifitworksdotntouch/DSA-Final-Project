import requests # pyright: ignore[reportMissingModuleSource]
import threading
from dataclasses import dataclass
from typing import Callable, List, Optional

BASE_URL = "http://localhost:8080"
TIMEOUT  = 5

@dataclass
class SortStep:
    array: List[int]
    pivot_index: Optional[int]
    compare_indices: List[int]
    swap_indices: List[int]
    sorted_indices: List[int]
    left: int
    right: int
    depth: int
    comparisons: int
    swaps: int
    message: str

    @staticmethod
    def from_dict(d: dict) -> "SortStep":
        return SortStep(
            array = d["array"],
            pivot_index = d.get("pivotIndex"),
            compare_indices = d.get("compareIndices", []),
            swap_indices = d.get("swapIndices", []),
            sorted_indices = d.get("sortedIndices", []),
            left = d.get("left", 0),
            right = d.get("right", 0),
            depth  = d.get("depth", 0),
            comparisons = d.get("comparisons", 0),
            swaps = d.get("swaps", 0),
            message = d.get("message", ""),
        )

@dataclass
class SortResult:
    steps: List[SortStep]
    total_comparisons: int
    total_swaps: int
    max_depth: int
    
    @staticmethod
    def from_dict(d: dict) -> "SortResult":
        return SortResult(
            steps = [SortStep.from_dict(s) for s in d["steps"]],
            total_comparisons = d.get("totalComparisons", 0),
            total_swaps = d.get("totalSwaps", 0),
            max_depth = d.get("maxDepth", 0),
        )

class SortApiClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()

    def sort(self, array: List[int]) -> SortResult:
        resp = self._session.post(
            f"{self.base_url}/sort",
            json={"array": array},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        return SortResult.from_dict(resp.json())

    def random_array(self, size: int = 10, min_val: int = 1, max_val: int = 99) -> List[int]:
        try:
            resp = self._session.get(
                f"{self.base_url}/array/random",
                params={"size": size, "min": min_val, "max": max_val},
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception:
            import random
            return [random.randint(min_val, max_val) for _ in range(size)]

    def health(self) -> bool:
        try:
            resp = self._session.get(f"{self.base_url}/health", timeout=2)
            return resp.status_code == 200
        except Exception:
            return False

    def sort_async(self, array: List[int],
                   on_success: Callable[[SortResult], None],
                   on_error: Callable[[str], None], tk_root):
        def _worker():
            try:
                result = self.sort(array)
                tk_root.after(0, lambda: on_success(result))
            except requests.ConnectionError:
                tk_root.after(0, lambda: on_error(
                    f"Cannot reach backend.\nIs Spring Boot running on {self.base_url}?"))
            except requests.HTTPError as e:
                msg = f"Backend error: {e.response.status_code}"
                try:
                    body = e.response.json()
                    if isinstance(body, dict) and body.get("error"):
                        msg = str(body["error"])
                except Exception:
                    pass
                tk_root.after(0, lambda m=msg: on_error(m))
            except Exception as e:
                tk_root.after(0, lambda: on_error(str(e)))
        threading.Thread(target=_worker, daemon=True).start()

    def random_array_async(self, on_success: Callable[[List[int]], None],
                           on_error: Callable[[str], None],
                           tk_root, size: int = 10):
        def _worker():
            try:
                arr = self.random_array(size=size)
                tk_root.after(0, lambda: on_success(arr))
            except Exception as e:
                tk_root.after(0, lambda: on_error(str(e)))
        threading.Thread(target=_worker, daemon=True).start()