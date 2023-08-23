import { Avatar, Box, Group, Stack, Text } from "@mantine/core";
import demoAvatarImage from "../../assets/avata.jpeg";
import { useQuery } from "@tanstack/react-query";
import {
  getAllThreadsQueryKey,
  requestGetAllThreads,
} from "../../services/forum/get-all-thread.ts";
import { AnswerForm } from "../answer-form";

export function ThreadComments({ id }: { id: string | number }) {
  const { data } = useQuery(getAllThreadsQueryKey(id), () =>
    requestGetAllThreads(id),
  );
  return (
    <Stack>
      {data &&
        data.results.map((threadModel) => (
          <Stack key={threadModel.pk}>
            <Avatar src={demoAvatarImage} color="blue" radius="sm" size="sm" />
            <Text>Commented at {threadModel?.fields?.created}</Text>
            <Box>
              {threadModel?.fields?.content && (
                <div
                  dangerouslySetInnerHTML={{
                    __html: threadModel.fields.content,
                  }}
                />
              )}
            </Box>
          </Stack>
        ))}
      <AnswerForm id={id} title="Comment" />
    </Stack>
  );
}
