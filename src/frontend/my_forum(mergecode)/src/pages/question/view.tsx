import { NavLink, useParams } from "react-router-dom";
import {
  ActionIcon,
  Avatar,
  Badge,
  Box,
  Button,
  Divider,
  Group,
  LoadingOverlay,
  Paper,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { IconThumbUp, IconThumbDown } from "@tabler/icons-react";
import demoAvatarImage from "../../assets/avata.jpeg";
import { useQuery } from "@tanstack/react-query";
import {
  getThreadQueryKey,
  requestGetThread,
} from "../../services/forum/get-thread.ts";
import {
  requestGetThreadTags,
  threadTagsQueryKey,
} from "../../services/forum/get-thread-tags.ts";
import { AnswerForm } from "../../components/answer-form";
import { ThreadAnswers } from "../../components/thread-answers/thread-answers.tsx";
import { ThreadComments } from "../../components/thread-comments";


const items = [1];

export function ViewQuestionPage() {
  const { id } = useParams<"id">();
  const { data, isLoading } = useQuery(
    getThreadQueryKey(id || ""),
    () => requestGetThread(id || ""),
    {
      enabled: !!id,
    },
  );
  const { data: tagsData } = useQuery(threadTagsQueryKey, () =>
    requestGetThreadTags(id || ""),
  );
  
  return (
    <Box>
      <LoadingOverlay visible={isLoading} />
      <Group position="apart">
        <Box>
          <Title fw={400}>{data?.fields?.title}</Title>
          <Text fz="xs">Asked at {data?.fields?.created}</Text>
        </Box>
        <Box>
          <NavLink to="/question/create">
            <Button>Ask question</Button>
          </NavLink>
        </Box>
      </Group>
      <Paper withBorder p="xl" mb="xl">
        <Group align="start">
          <Box>
            <Stack align="center">
              <ActionIcon color="blue" size="lg" radius="xl" variant="outline">
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
              <Group>
                <Avatar src={demoAvatarImage} color="blue" radius="sm" />
                {data?.fields?.creator_name || data?.fields?.creator_email}
              </Group>
              <Box>
                {data?.fields?.content && (
                  <div
                    dangerouslySetInnerHTML={{
                      __html: data.fields.content,
                    }}
                  />
                  )}
              </Box>
              <Group spacing="sm">
                {tagsData &&
                  tagsData.results.map((tagModel) => (
                    <Badge key={tagModel.pk}>{tagModel.fields.tag_name}</Badge>
                  ))}
              </Group>
              <Group>
                Approved by:{" "}
                {data?.fields?.approver_name || data?.fields?.approver_email}
              </Group>
              <Group>
                <Button>Report</Button>
              </Group>
            </Stack>
            <Divider my="md" />
            {id && <ThreadComments id={id} />}
          </Box>
        </Group>
      </Paper>
      {id && <ThreadAnswers id={id} />}
      {id && <AnswerForm id={id} title="Your answer" />}
    </Box>
  );
}
