# Baseball Analytics Technical Questions

This repository contains solutions to baseball analytics interview questions covering data engineering, model serving, SQL, system design, and baseball-specific modeling.

## Questions Covered

1. **Q1 - Streaming Pitch Data → Rolling Features** ✓
   - Real-time per-pitcher rolling statistics (velocity, zone rate, whiff rate)
   - O(1) amortized updates with bounded memory

2. **Q2 - Model Serving: Batched Inference API**
   - GPU-efficient batched predictions with <100ms latency
   - Thread-safe request handling with timeout guarantees

3. **Q3 - SQL: Deduplicate and Choose Latest Model Version**
   - Window functions for finding latest model runs
   - Ranking queries for best model selection

4. **Q4 - System Design: End-to-End ML Pipeline**
   - Production ML pipeline architecture
   - Versioning, rollback, and monitoring strategies

5. **Q5 - In-Game Win Probability Update**
   - Run expectancy calculations
   - Feature engineering for win probability models

## Setup Instructions

### 1. Activate Virtual Environment

The project already has a virtual environment set up. Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch Jupyter Notebook

```bash
jupyter notebook
```

This will open Jupyter in your browser. Open `baseball_analytics_questions.ipynb` to see the solutions.

### 4. Alternative: Use Jupyter Lab

For a more modern interface:

```bash
pip install jupyterlab
jupyter lab
```

## Project Structure

```
baseball-analytics-questions/
├── venv/                           # Virtual environment
├── requirements.txt                # Python dependencies
├── baseball_analytics_questions.ipynb  # Main notebook with solutions
├── README.md                       # This file
└── rolling_stats.png              # Generated visualization (after running Q1)
```

## Dependencies

### Core Libraries
- **jupyter/notebook**: Interactive notebook environment
- **pandas/numpy**: Data manipulation and numerical computing
- **matplotlib/seaborn**: Data visualization

### Machine Learning
- **scikit-learn**: ML utilities and modeling
- **xgboost**: Gradient boosting framework (for Q4)

### Database & API
- **psycopg2-binary**: PostgreSQL adapter (for Q3)
- **sqlalchemy**: SQL toolkit
- **fastapi/uvicorn**: API framework (for Q2)

### Testing
- **pytest**: Testing framework

## Running the Solutions

### Q1 - Rolling Pitch Statistics

The Q1 solution is complete and ready to run. In the notebook:

1. Run the import cell
2. Run the `PitcherRollingStats` class definition
3. Execute the test data generation
4. Process the pitch stream and view results
5. Generate visualizations

The solution demonstrates:
- O(1) amortized updates using `deque` with fixed max length
- Bounded memory (100 pitches per pitcher)
- Handling multiple pitchers interleaved in the stream
- Edge case handling (division by zero, varying pitch counts)

### Q2-Q5

Solutions for remaining questions are structured in the notebook with TODO sections. Add your implementations in the designated cells.

## Testing

To verify the Q1 implementation:

```python
# In the notebook or Python console
from collections import deque, defaultdict

stats = PitcherRollingStats(window=100)

# Test single pitcher
for i in range(150):
    event = {
        'pitcher_id': 'P1',
        'velocity': 92.5,
        'is_in_zone': i % 2,
        'is_swing': i % 3 == 0,
        'is_whiff': i % 6 == 0
    }
    result = stats.update(event)

# Verify window size is bounded at 100
assert result['pitch_count'] == 100
```

## Performance Characteristics

### Q1 Solution
- **Time**: O(1) amortized per `update()` call
- **Space**: O(P × W) where P = pitchers, W = window (100)
- **Window calculation**: O(W) but W is constant, so effectively O(1)

## Notes

- All visualizations are saved to the project directory
- The notebook includes extensive comments and explanations
- Test data generators are included for validation
- Solutions follow baseball analytics best practices

## Next Steps

1. Complete Q2-Q5 implementations
2. Add more comprehensive test cases
3. Benchmark performance with larger datasets
4. Integrate with real Statcast data sources
5. Deploy Q2 API solution with Docker

## Resources

- [Statcast Data](https://baseballsavant.mlb.com/statcast_search)
- [Run Expectancy Tables](https://library.fangraphs.com/misc/re24/)
- [Win Probability Models](https://library.fangraphs.com/misc/wpa/)
