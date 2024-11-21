from .signup import signup_view
from .login import LoginView
from .profile import (
    create_profile,
    ProfileDetailView,
    ProfileUpdateView
)
from .place import (
    NearbyCafeListView,
    CafeDetailView,
    add_rating,
    ReviewListCreateView,
    ReviewDetailView,
)

from .board import get_board
from .post import PostListView, PostDetailView
from .comment import CommentListView, CommentDetailView
