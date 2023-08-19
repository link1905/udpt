import {
  Box,
  Button,
  Input,
  List,
  LoadingOverlay,
  Paper,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { DetailEditor } from "../../components/create-question-form/detail-editor";
import { TagsInput } from "../../components/create-question-form/tags-input";
import { useForm } from "@mantine/form";
import { CategoryInput } from "../../components/create-question-form/category-input";
import { useMutation } from "@tanstack/react-query";
import { requestCreateThread } from "../../services/forum/create-thread.ts";
import { CreateThreadForm } from "../../services/forum/forum.client.ts";
import { useNavigate } from "react-router-dom";
import { requestCreateTaggedThread } from "../../services/forum/create-tagged-thread.ts";

export interface CreateQuestionData extends CreateThreadForm {
  title: string;
  content: string;
  tags: number[];
  category: number;
}

export function CreateQuestionPage() {
  const navigate = useNavigate();

  const { mutate, isLoading } = useMutation(
    async ({ tags, ...data }: CreateQuestionData) => {
      const thread = await requestCreateThread(data);
      for (const tag of tags) {
        await requestCreateTaggedThread({
          tag_id: tag,
          thread: thread.pk,
        });
      }
      return thread;
    },
    {
      onSuccess(data) {
        navigate(`/question/${data.pk}`);
      },
    },
  );
  const form = useForm<CreateQuestionData>({
    initialValues: {
      title: "",
      content: "------",
      tags: [],
      category: 0,
    },
    validate: {
      title: (value) => (!value ? "Title is required " : null),
      category: (value) => (!value ? "Category is required " : null),
      content: (value) => (!value ? "Content is required " : null),
    },
  });

  return (
    <Box
      pb={100}
      component="form"
      onSubmit={form.onSubmit((values) => mutate(values))}
    >
      <LoadingOverlay visible={isLoading} />
      <Title mb="xl">Ask a question</Title>
      <Stack spacing="lg">
        <Paper withBorder p="xl">
          <Title order={4}>Writing a good question</Title>
          <Text fz="sm">
            You’re ready to ask a programming-related question and this form
            will help guide you through the process. Looking to ask a
            non-programming question? See the topics here to find a relevant
            site.
          </Text>
          <br />
          <Text fz="sm" fw="bold">
            Steps
          </Text>
          <List>
            <List.Item fz="sm">
              Summarize your problem in a one-line title.
            </List.Item>
            <List.Item fz="sm">Describe your problem in more detail.</List.Item>
            <List.Item fz="sm">
              Describe what you tried and what you expected to happen.
            </List.Item>
            <List.Item fz="sm">
              Add “tags” which help surface your question to members of the
              community.
            </List.Item>
            <List.Item fz="sm">
              Review your question and post it to the site
            </List.Item>
          </List>
        </Paper>
        <Paper withBorder p="xl">
          <Input.Wrapper
            mb="md"
            withAsterisk
            label="Title"
            description="Be specific and imagine you’re asking a question to another person."
          >
            <Input
              {...form.getInputProps("title")}
              placeholder="e.g. Is there an R function for finding the index of an element in a vector?"
            />
          </Input.Wrapper>
        </Paper>
        <Paper withBorder p="xl">
          <Input.Wrapper
            mb="md"
            withAsterisk
            label="What are the details of your problem?"
            description="Introduce the problem and expand on what you put in the title. Minimum 20 characters."
          >
            <Box mt="sm">
              <DetailEditor {...form.getInputProps("content")} />
            </Box>
          </Input.Wrapper>
        </Paper>
        <Paper withBorder p="xl">
          <Input.Wrapper
            mb="md"
            withAsterisk
            label="Tags"
            description="Add up to 5 tags to describe what your question is about. Start typing to see suggestions."
          >
            <Box mt="sm">
              <TagsInput {...form.getInputProps("tags")} />
            </Box>
          </Input.Wrapper>
        </Paper>
        <Paper withBorder p="xl">
          <Input.Wrapper
            mb="md"
            withAsterisk
            label="Category"
            description="Select a category"
          >
            <Box mt="sm">
              <CategoryInput {...form.getInputProps("category")} />
            </Box>
          </Input.Wrapper>
        </Paper>
        <Box>
          <Button type="submit">Submit question</Button>
        </Box>
      </Stack>
    </Box>
  );
}
