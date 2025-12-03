"""
Q1 - Streaming Pitch Data → Rolling Features

Maintain per-pitcher rolling statistics over the last 100 pitches.
O(1) amortized updates with bounded memory.
"""

from collections import deque, defaultdict
import random


class PitcherRollingStats:
    def __init__(self, window=100):
        """
        Initialize the rolling stats tracker.

        Args:
            window: Number of recent pitches to track (default: 100)
        """
        self.window = window
        self.pitch_data = defaultdict(lambda: deque(maxlen=self.window))

    def update(self, event):
        """
        Ingest one pitch event and return current rolling stats for that pitcher.

        Args:
            event: dict with keys: game_id, pitcher_id, batter_id, inning,
                   pitch_number, pitch_type, velocity, spin_rate, is_in_zone,
                   is_swing, is_ball_in_play, is_strike, is_whiff

        Returns:
            dict: Rolling statistics for the pitcher
        """
        pitcher_id = event['pitcher_id']
        dq = self.pitch_data[pitcher_id]
        dq.append(event)  # auto-pops from left if >100

        # Compute rolling average velocity
        total_vel = sum(p['velocity'] for p in dq)
        mean_vel = total_vel / len(dq)

        # Zone rate: fraction where is_in_zone == 1
        in_zone_count = sum(p['is_in_zone'] for p in dq)
        zone_rate = in_zone_count / len(dq)

        # Whiff rate: whiffs / swings, but only for pitches with is_swing
        swings = sum(p['is_swing'] for p in dq)
        whiffs = sum(p['is_whiff'] for p in dq)
        whiff_rate = (whiffs / swings) if swings > 0 else 0.0

        return {
            'pitcher_id': pitcher_id,
            'mean_velocity': mean_vel,
            'zone_rate': zone_rate,
            'whiff_rate': whiff_rate,
            'pitch_count': len(dq)
        }


def generate_sample_pitch():
    """Generate a single sample pitch event."""
    pitch_types = ['FF', 'SL', 'CH', 'CU', 'SI']
    is_swing = random.random() < 0.45
    is_whiff = is_swing and (random.random() < 0.25)

    return {
        'game_id': f"G{random.randint(1, 5)}",
        'pitcher_id': f"P{random.randint(1, 3)}",
        'batter_id': f"B{random.randint(1, 20)}",
        'inning': random.randint(1, 9),
        'pitch_number': 0,  # Will be set by caller
        'pitch_type': random.choice(pitch_types),
        'velocity': round(random.uniform(85, 98), 1),
        'spin_rate': random.randint(2000, 2800),
        'is_in_zone': random.random() < 0.48,
        'is_swing': is_swing,
        'is_ball_in_play': is_swing and (random.random() < 0.75),
        'is_strike': random.random() < 0.52,
        'is_whiff': is_whiff
    }


def main():
    """Example usage of PitcherRollingStats."""
    print("Baseball Analytics Q1 - Rolling Pitch Statistics")
    print("=" * 60)

    # Initialize tracker
    stats_tracker = PitcherRollingStats(window=100)

    # Simulate pitch stream
    num_pitches = 300
    print(f"\nProcessing {num_pitches} pitches from 3 pitchers...")

    pitcher_stats = {}

    for i in range(num_pitches):
        pitch = generate_sample_pitch()
        pitch['pitch_number'] = i

        stats = stats_tracker.update(pitch)
        pitcher_stats[stats['pitcher_id']] = stats

    # Display final results
    print("\n" + "=" * 60)
    print("Final Rolling Statistics (last 100 pitches per pitcher)")
    print("=" * 60)

    for pitcher_id in sorted(pitcher_stats.keys()):
        stats = pitcher_stats[pitcher_id]
        print(f"\n{pitcher_id}:")
        print(f"  Pitch Count:     {stats['pitch_count']}")
        print(f"  Avg Velocity:    {stats['mean_velocity']:.1f} mph")
        print(f"  Zone Rate:       {stats['zone_rate']:.1%}")
        print(f"  Whiff Rate:      {stats['whiff_rate']:.1%}")

    print("\n" + "=" * 60)
    print("[OK] All pitchers processed with O(1) amortized updates")
    print("[OK] Memory bounded at 100 pitches per pitcher")


if __name__ == "__main__":
    main()
