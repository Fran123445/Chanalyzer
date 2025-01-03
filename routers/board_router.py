from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/board"
)

@router.post("/{board_name}/embedding/semantic")
def post_embedding(board_name: str, request: Request):
    request.app.state.semantic_processor.process_board(board_name)
    return {"message": f"{board_name} processed"}