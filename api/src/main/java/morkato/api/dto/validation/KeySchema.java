package morkato.api.dto.validation;

import org.hibernate.validator.constraints.Length;
import jakarta.validation.constraints.Pattern;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.ElementType;
import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import jakarta.validation.Constraint;
import java.lang.annotation.Target;
import jakarta.validation.Payload;

@Length(min = 2, max = 32)
@Pattern(regexp = "^[^:0-9\\s][^:\\s]{1,31}$")
@Target({ ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER, ElementType.ANNOTATION_TYPE })
@Retention(RetentionPolicy.RUNTIME) 
@Documented
@Constraint(validatedBy = {})
public @interface KeySchema {
  String message() default "This key is invalid!";
  Class<?>[] groups() default {};
  Class<? extends Payload>[] payload() default {};
}