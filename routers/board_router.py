from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/board"
)

@router.post("/{board_name}/embedding/semantic")
def post_embedding(board_name: str, request: Request):
    request.app.state.semantic_processor.process_board(board_name)
    return {"message": f"{board_name} processed"}

@router.get("/{board_name}/similar/semantic")
def get_similar_to_board(board_name: str, request:Request, top_n = 10):
    return request.app.state.board_finder.find_similar_to_board(board_name, top_n)

@router.get("/similar/semantic")
def get_similar_to_texts(text_list: list[str], weights_list: list[int], request: Request, top_n = 10):
    return request.app.state.board_finder.find_similar_to_text_list(text_list, weights_list, top_n)