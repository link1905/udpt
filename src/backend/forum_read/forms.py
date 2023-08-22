from typing import Optional
from django import forms
from django.core.exceptions import ValidationError
from forum.models import TaggedThread, Thread, ThreadCategory, ThreadVote
from tag.services import get_tag


class ThreadForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        Thread.objects.live().filter(
            Thread.objects.question_q() | Thread.objects.answer_q()
        ),
        required=False,
    )

    def _pre_clean_creator_fields(self) -> None:
        if self.instance.pk is not None:
            self["creator_id"].field.disabled = True
            self["creator_name"].field.disabled = True
            self["creator_email"].field.disabled = True

    def _pre_clean_category_fields(self) -> None:
        if self.instance.pk is not None:
            self["category"].field.disabled = True

    def _pre_clean_parent_fields(self) -> None:
        if self.instance.pk is not None:
            self["parent"].field.disabled = True

    def _post_clean_body_fields(self) -> None:
        if self.has_changed:
            self.instance.approver_id = 0
            self.instance.approved = False
            self.instance.approver_name = ""
            self.instance.approver_email = ""

    def _post_clean_category_fields(self) -> None:
        if (
            self.cleaned_data["parent"] is not None
            and self.cleaned_data["category"] is not None
        ):
            self.add_error("category", ValidationError(
                "category cannot be set on an answer or comment",
                code="invalid",
            ))

    def _clean_fields(self) -> None:
        self._pre_clean_creator_fields()
        self._pre_clean_parent_fields()
        self._pre_clean_category_fields()
        super()._clean_fields()

        if self.errors:
            return

        self._post_clean_body_fields()
        self._post_clean_category_fields()

    class Meta:
        model = Thread
        fields = (
            "title",
            "content",
            "creator_id",
            "creator_name",
            "creator_email",
            "category",
            "parent",
        )


class ThreadStaffForm(ThreadForm):
    def _pre_clean_approver_fields(self) -> None:
        if self.instance.pk is None or self.instance.approved:
            self["approved"].field.disabled = True
            self["approver_id"].field.disabled = True
            self["approver_name"].field.disabled = True
            self["approver_email"].field.disabled = True

    def _post_clean_approved_fields(self) -> None:
        approved = self.cleaned_data["approved"]
        if approved and not self.cleaned_data["approver_id"]:
            self.add_error(
                "approved",
                ValidationError(
                    "an approver is required to approve a thread", code="required"
                ),
            )

    def _clean_fields(self) -> None:
        self._pre_clean_approver_fields()
        super()._clean_fields()

        if self.errors:
            return

        self._post_clean_approved_fields()


    class Meta:
        model = Thread
        fields = (
            "title",
            "content",
            "creator_id",
            "creator_name",
            "creator_email",
            "approver_id",
            "approved",
            "approver_name",
            "approver_email",
            "parent",
            "category",
        )


class ThreadVoteForm(forms.ModelForm):
    thread = forms.ModelChoiceField(
        Thread.objects.live(),
        required=True,
    )

    def _pre_clean_user_fields(self) -> None:
        if self.instance.pk is not None:
            self["user_id"].field.disabled = True
            self["user_name"].field.disabled = True
            self["user_email"].field.disabled = True

    def _pre_clean_thread_fields(self) -> None:
        if self.instance.pk is not None:
            self["thread"].field.disabled = True

    def _clean_fields(self) -> None:
        self._pre_clean_user_fields()
        self._pre_clean_thread_fields()
        super()._clean_fields()

    class Meta:
        model = ThreadVote
        fields = (
            "user_id",
            "user_name",
            "user_email",
            "thread",
            "is_upvote",
        )


class TaggedThreadForm(forms.ModelForm):
    creator_id = forms.IntegerField(required=True)

    def clean_tag_id(self) -> int:
        tag_id = self.cleaned_data["tag_id"]
        tag = get_tag(tag_id)

        if tag is None:
            self.add_error(
                "tag_id", ValidationError("tag does not exist", code="invalid")
            )
            return tag_id

        self.instance.tag_name = tag.fields.name
        return tag_id

    def _pre_clean_readonly_fields(self) -> None:
        if self.instance.pk is not None:
            self["thread"].field.disabled = True
            self["tag_id"].field.disabled = True
            self["user_id"].field.disabled = True


    def _post_clean_creator_id(self) -> None:
        creator_id = self.cleaned_data["creator_id"]

        if self.cleaned_data["thread"].creator_id != creator_id:
            self.add_error(
                "creator_id",
                ValidationError("user does not own thread", code="invalid"),
            )


    def _clean_fields(self) -> None:
        self._pre_clean_readonly_fields()
        super()._clean_fields()
        if self.errors:
            return

        self._post_clean_creator_id()

    class Meta:
        model = TaggedThread
        fields = ("thread", "tag_id", "creator_id")


class ThreadCategoryForm(forms.ModelForm):
    class Meta:
        model = ThreadCategory
        fields = ("name",)
