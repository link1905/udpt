import { forumServiceClient } from "./forum.client.ts";

export const requestCreateTaggedThread = (data: {
  thread: number;
  tag_id: number;
}) =>
  forumServiceClient
    .post("/models/tagged-threads/records/", data)
    .then((res) => res.data);
