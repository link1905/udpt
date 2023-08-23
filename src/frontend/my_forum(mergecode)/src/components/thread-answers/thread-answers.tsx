import { useQuery } from "@tanstack/react-query";
import {
  getAllThreadsQueryKey,
  requestGetAllThreads,
} from "../../services/forum/get-all-thread.ts";
import {
  ActionIcon,
  Avatar,
  Box,
  Divider,
  Group,
  Paper,
  Stack,
  Text,
} from "@mantine/core";
import { IconThumbDown, IconThumbUp } from "@tabler/icons-react";
import demoAvatarImage from "../../assets/avata.jpeg";
import { ThreadComments } from "../thread-comments";

export function ThreadAnswers({ id }: { id: string }) {
  const { data } = useQuery(getAllThreadsQueryKey(id), () =>
    requestGetAllThreads(id),
  );
  return (
    <Stack>
      {data &&
        data.results.map((threadModel) => (
          <Paper key={threadModel.pk} withBorder p="xl" mb="xl">
            <Group align="start">
              <Box>
                <Stack align="center">
                  <ActionIcon
                    color="blue"
                    size="lg"
                    radius="xl"
                    variant="outline"
                  >
                    <IconThumbUp size="1.625rem" />
                  </ActionIcon>
                  <Text fz="lg" fw={600}>
                    99
                  </Text>
                  <ActionIcon size="lg" radius="xl" variant="outline">
                    <IconThumbDown size="1.625rem" />
                  </ActionIcon>
                </Stack>
              </Box>
              <Box sx={{ flex: 1 }}>
                <Stack align="start">
                  <Text>Answer at {threadModel?.fields?.created}</Text>
                  <Group>
                    <Avatar src={demoAvatarImage} color="blue" radius="sm" />
                    {threadModel?.fields?.creator_name ||
                      threadModel?.fields?.creator_email}
                  </Group>
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
                <Divider my="md" />
                <ThreadComments id={threadModel.pk} />
              </Box>
            </Group>
          </Paper>
        ))}
    </Stack>
  );
}
