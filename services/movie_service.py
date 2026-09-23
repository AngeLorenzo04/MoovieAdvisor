from sqlalchemy.orm import Session
from sqlalchemy import not_
from models import Movie, User, UserInteraction, InteractionStatus, MoodType

def get_or_create_user(db: Session, telegram_id: int) -> User:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def get_next_movie(db: Session, user: User, mood: MoodType, max_runtime: int = None, min_runtime: int = None):
    # Exclude movies the user has interacted with (SEEN, CHOSEN, or SKIPPED)
    excluded_interactions = db.query(UserInteraction.movie_id).filter(
        UserInteraction.user_id == user.id
    ).all()
    
    excluded_ids = [interaction[0] for interaction in excluded_interactions]

    tier_filter = Movie.tier <= user.current_tier if user.include_lower_tiers else Movie.tier == user.current_tier

    query = db.query(Movie).filter(
        Movie.mood_tag == mood,
        tier_filter,
        not_(Movie.id.in_(excluded_ids)) if excluded_ids else True
    )

    if max_runtime:
        query = query.filter(Movie.runtime <= max_runtime)
    if min_runtime:
        query = query.filter(Movie.runtime > min_runtime)

    # In a real app we might want to randomize this, but let's just get the first available
    return query.first()

def log_interaction(db: Session, user_id: int, movie_id: int, status: InteractionStatus):
    interaction = UserInteraction(
        user_id=user_id,
        movie_id=movie_id,
        status=status
    )
    db.add(interaction)
    db.commit()
    return interaction

def get_user_stats(db: Session, user: User):
    # Calculate stats for the /skills command
    seen_movies = db.query(UserInteraction).filter(
        UserInteraction.user_id == user.id,
        UserInteraction.status.in_([InteractionStatus.SEEN, InteractionStatus.CHOSEN])
    ).all()
    
    total_seen = len(seen_movies)
    
    # Calculate tier progress (simplified logic: e.g., need 5 movies to unlock tier 2)
    movies_needed_for_tier_2 = 5
    tier_progress = min(100, int((total_seen / movies_needed_for_tier_2) * 100))
    
    return {
        "current_tier": user.current_tier,
        "total_seen": total_seen,
        "tier_progress": tier_progress,
        "movies_needed_for_tier_2": movies_needed_for_tier_2
    }
