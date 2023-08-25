import { forumServiceClient } from "./forum.client";
import { UpdateThread } from "./forum.client";

export const requestUpdateThread = (id: number, data: Partial<UpdateThread>) =>
  forumServiceClient
    .put<UpdateThread>(`/models/threads/records/${id}/`, data)
    .then((res) => res.data);
