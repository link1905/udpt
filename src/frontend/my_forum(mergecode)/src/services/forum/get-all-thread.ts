import { forumServiceClient, ThreadFields } from "./forum.client.ts";
import { ListResponse } from "../client.ts";
//export const requestGetAllThreads = (): Promise<ListResponse<ThreadFields>> =>
//forumServiceClient
//.get<ListResponse<ThreadFields>>(`/models/threads/records/`)
//.then((res) => res.data);

//requestGetAllThreads()
//.then((threadsResponse) => {
//const threads = threadsResponse.results;
//console.log(threads);
//})
//.catch((error) => {
//console.error("Error fetching threads:", error);
//});
//
export const requestGetAllThreads = (parent: string | number) =>
  forumServiceClient
    .get<ListResponse<ThreadFields>>(
      `/models/threads/records/` + (parent ? `?parent=${parent}` : ""),
      {
        params: {
          include_approved_status: true, 
        },
      }
    )
    .then((res) => res.data);

export const requestGetLatestThreads = () =>
  forumServiceClient
    .get<ListResponse<ThreadFields>>(`/models/threads/records/`, {
      params: {
        ordering: "-fields.created",
      },
    })
    .then((res) => res.data);

export const getAllThreadsQueryKey = (parent: string | number) =>
  parent ? ["thread", parent, "child"] : ["thread"];
