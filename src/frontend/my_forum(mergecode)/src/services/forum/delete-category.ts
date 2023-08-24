import { forumServiceClient } from "./forum.client";

export const requestDeleteCategory = (pk: number) =>
  forumServiceClient
    .delete(`/models/thread-categories/records/${pk}/`)
    .then((res) => res.data)
    .catch((error) => {
      throw new Error(`Error deleting category: ${error}`);
    });
